from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.db.models import Recention


@pytest.fixture
def app(override_get_db):
    from app.db.config import get_db
    from app.main import app
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestRecentionsController:
    @pytest.mark.unit
    @patch("app.controllers.recentions.RecentionsDAO")
    @patch("app.controllers.recentions.required_user")
    def test_get_recentions_by_me(self, mock_required_user, mock_recentions_dao, client, db_session, test_user, test_movie, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user

        test_recention = Recention(
            id=uuid4(),
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great!",
        )
        test_recention.movie = test_movie
        mock_recentions_dao.find_all_by_user_id = AsyncMock(return_value=[test_recention])

        response = client.get("/recentions/users/me")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["rate"] == 8

    @pytest.mark.unit
    @patch("app.controllers.recentions.get_recention")
    @patch("app.controllers.recentions.required_user")
    def test_get_recention_by_id_success(self, mock_required_user, mock_get_recention, client, db_session, test_user, test_recention, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        test_recention.movie = test_recention.movie
        mock_get_recention.return_value = test_recention

        response = client.get(f"/recentions/{test_recention.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_recention.id)
        assert data["rate"] == test_recention.rate

    @pytest.mark.unit
    @patch("app.controllers.recentions.MoviesDAO")
    @patch("app.controllers.recentions.RecentionsDAO")
    @patch("app.controllers.recentions.check_recention")
    @patch("app.controllers.recentions.get_recention")
    @patch("app.controllers.recentions.required_user")
    def test_create_recention_success(
        self, mock_required_user, mock_get_recention, mock_check_recention,
        mock_recentions_dao, mock_movies_dao, client, db_session, test_user, test_movie, app
    ):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_movies_dao.find_by_id = AsyncMock(return_value=test_movie)

        new_recention = Recention(
            id=uuid4(),
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great!",
        )
        new_recention.movie = test_movie
        mock_recentions_dao.add = AsyncMock(return_value=new_recention)
        mock_get_recention.return_value = new_recention

        response = client.post(
            "/recentions/create",
            json={
                "movie_id": str(test_movie.id),
                "rate": 8,
                "movie_status": "watched",
                "comment": "Great!",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["rate"] == 8
        assert data["movie_status"] == "watched"

    @pytest.mark.unit
    @patch("app.controllers.recentions.MoviesDAO")
    @patch("app.controllers.recentions.required_user")
    def test_create_recention_movie_not_found(self, mock_required_user, mock_movies_dao, client, db_session, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_movies_dao.find_by_id = AsyncMock(return_value=None)

        response = client.post(
            "/recentions/create",
            json={
                "movie_id": str(uuid4()),
                "rate": 8,
                "movie_status": "watched",
                "comment": "Great!",
            },
        )

        assert response.status_code == 404
        assert "not found" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.recentions.RecentionsDAO")
    @patch("app.controllers.recentions.check_recention")
    @patch("app.controllers.recentions.get_recention")
    @patch("app.controllers.recentions.required_user")
    def test_update_recention_success(
        self, mock_required_user, mock_get_recention, mock_check_recention,
        mock_recentions_dao, client, db_session, test_user, test_recention, test_movie, app
    ):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_get_recention.return_value = test_recention

        updated_recention = Recention(
            id=test_recention.id,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=9,
            movie_status="watched",
            comment="Updated!",
        )
        updated_recention.movie = test_movie
        mock_recentions_dao.update = AsyncMock(return_value=updated_recention)

        response = client.put(
            f"/recentions/{test_recention.id}",
            json={
                "rate": 9,
                "movie_status": "watched",
                "comment": "Updated!",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["rate"] == 9
        assert data["comment"] == "Updated!"

    @pytest.mark.unit
    @patch("app.controllers.recentions.RecentionsDAO")
    @patch("app.controllers.recentions.get_recention")
    @patch("app.controllers.recentions.required_user")
    def test_delete_recention_success(
        self, mock_required_user, mock_get_recention,
        mock_recentions_dao, client, db_session, test_user, test_recention, app
    ):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_get_recention.return_value = test_recention
        mock_recentions_dao.delete = AsyncMock()

        response = client.delete(f"/recentions/{test_recention.id}")

        assert response.status_code == 204
        mock_recentions_dao.delete.assert_called_once()

