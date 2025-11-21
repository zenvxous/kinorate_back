from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.models import User


@pytest.fixture
def app(override_get_db):
    from app.db.config import get_db
    from app.main import app
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestUsersController:
    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    @patch("app.controllers.users.check_user")
    @patch("app.controllers.users.hash_password")
    def test_register_user_success(self, mock_hash_password, mock_check_user, mock_users_dao, client, db_session, override_get_db):
        mock_hash_password.return_value = "hashed_password"
        mock_users_dao.get_by_email_or_nickname = AsyncMock(return_value=[])
        mock_users_dao.add = AsyncMock(return_value=MagicMock())

        response = client.post(
            "/users/register",
            data={
                "email": "test@example.com",
                "nickname": "testuser",
                "password": "password123",
            },
        )

        assert response.status_code == 201
        mock_check_user.assert_called_once()
        mock_users_dao.add.assert_called_once()

    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    @patch("app.controllers.users.check_user")
    def test_register_user_already_exists(self, mock_check_user, mock_users_dao, client, db_session, test_user):
        mock_users_dao.get_by_email_or_nickname = AsyncMock(return_value=[test_user])

        response = client.post(
            "/users/register",
            data={
                "email": test_user.email,
                "nickname": test_user.nickname,
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    @patch("app.controllers.users.verify_password")
    @patch("app.controllers.users.add_users_response_cookie")
    def test_login_user_success(self, mock_add_cookie, mock_verify_password, mock_users_dao, client, db_session, test_user):
        mock_users_dao.get_by_email = AsyncMock(return_value=test_user)
        mock_verify_password.return_value = True

        response = client.post(
            "/users/login",
            data={
                "email": test_user.email,
                "password": "password123",
            },
        )

        assert response.status_code == 204
        mock_verify_password.assert_called_once()
        mock_add_cookie.assert_called_once()

    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    def test_login_user_not_found(self, mock_users_dao, client, db_session):
        mock_users_dao.get_by_email = AsyncMock(return_value=None)

        response = client.post(
            "/users/login",
            data={
                "email": "nonexistent@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "invalid" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    @patch("app.controllers.users.verify_password")
    def test_login_user_wrong_password(self, mock_verify_password, mock_users_dao, client, db_session, test_user):
        mock_users_dao.get_by_email = AsyncMock(return_value=test_user)
        mock_verify_password.return_value = False

        response = client.post(
            "/users/login",
            data={
                "email": test_user.email,
                "password": "wrong_password",
            },
        )

        assert response.status_code == 400
        assert "invalid" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.users.settings")
    @patch("app.controllers.users.required_user")
    def test_logout_user(self, mock_required_user, mock_settings, client, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_settings.security.config.JWT_ACCESS_COOKIE_NAME = "_at"
        mock_settings.security.config.JWT_ACCESS_COOKIE_PATH = "/"
        mock_settings.security.config.JWT_COOKIE_DOMAIN = None
        mock_settings.security.config.JWT_COOKIE_SECURE = False
        mock_settings.security.config.JWT_COOKIE_SAMESITE = None
        mock_settings.security.config.JWT_COOKIE_CSRF_PROTECT = False

        response = client.post("/users/logout")

        assert response.status_code == 204

    @pytest.mark.unit
    @patch("app.controllers.users.required_user")
    def test_get_me(self, mock_required_user, client, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user

        response = client.get("/users/me")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_user.id)
        assert data["email"] == test_user.email
        assert data["nickname"] == test_user.nickname

    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    @patch("app.controllers.users.check_user")
    @patch("app.controllers.users.required_user")
    def test_update_me_success(self, mock_required_user, mock_check_user, mock_users_dao, client, db_session, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        updated_user = User(
            id=test_user.id,
            email="newemail@example.com",
            nickname="newnickname",
            password_hash=test_user.password_hash,
        )
        mock_users_dao.get_by_email_or_nickname = AsyncMock(return_value=[])
        mock_users_dao.update = AsyncMock(return_value=updated_user)

        response = client.put(
            "/users/me",
            json={
                "email": "newemail@example.com",
                "nickname": "newnickname",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"
        assert data["nickname"] == "newnickname"

    @pytest.mark.unit
    @patch("app.controllers.users.check_user")
    @patch("app.controllers.users.required_user")
    def test_update_me_no_changes(self, mock_required_user, mock_check_user, client, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user

        response = client.put(
            "/users/me",
            json={
                "email": test_user.email,
                "nickname": test_user.nickname,
            },
        )

        assert response.status_code == 400
        assert "no changes" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.users.RecentionsDAO")
    @patch("app.controllers.users.required_user")
    def test_get_my_stats(self, mock_required_user, mock_recentions_dao, client, db_session, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_recentions_dao.get_stats_by_user_id = AsyncMock(return_value={
            "movies_watched": 5,
            "average_rating": 8.5,
            "reviews_written": 3,
        })

        response = client.get("/users/me/stats")

        assert response.status_code == 200
        data = response.json()
        assert data["movies_watched"] == 5
        assert data["average_rating"] == 8.5
        assert data["reviews_written"] == 3

    @pytest.mark.unit
    @patch("app.controllers.users.UsersDAO")
    @patch("app.controllers.users.required_user")
    def test_delete_me(self, mock_required_user, mock_users_dao, client, db_session, test_user, app):
        from app.utils.session import required_user as req_user
        app.dependency_overrides[req_user] = lambda: test_user
        mock_required_user.return_value = test_user
        mock_users_dao.delete = AsyncMock()

        response = client.delete("/users/me")

        assert response.status_code == 204
        mock_users_dao.delete.assert_called_once()

