from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.models import Movie


@pytest.fixture
def app(override_get_db):
    from app.db.config import get_db
    from app.main import app
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestMoviesController:
    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    @patch("app.controllers.movies.check_genres")
    def test_create_movie_success(self, mock_check_genres, mock_movies_dao, client, db_session):
        mock_movies_dao.get_by_tmdb_id = AsyncMock(return_value=None)
        mock_check_genres.return_value = True

        from uuid import uuid4
        test_movie = Movie(
            id=uuid4(),
            tmdb_id=123,
            title="Test Movie",
            genres=["Action", "Drama"],
            poster_path="/poster.jpg",
        )
        mock_movies_dao.add = AsyncMock(return_value=test_movie)

        response = client.post(
            "/movies/create",
            json={
                "tmdb_id": 123,
                "title": "Test Movie",
                "genres": ["Action", "Drama"],
                "poster_path": "/poster.jpg",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["tmdb_id"] == 123
        assert data["title"] == "Test Movie"

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_create_movie_already_exists(self, mock_movies_dao, client, db_session, test_movie):
        mock_movies_dao.get_by_tmdb_id = AsyncMock(return_value=test_movie)

        response = client.post(
            "/movies/create",
            json={
                "tmdb_id": test_movie.tmdb_id,
                "title": "Test Movie",
                "genres": ["Action"],
                "poster_path": "/poster.jpg",
            },
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    @patch("app.controllers.movies.check_genres")
    def test_create_movie_invalid_genres(self, mock_check_genres, mock_movies_dao, client, db_session):
        mock_movies_dao.get_by_tmdb_id = AsyncMock(return_value=None)
        mock_check_genres.return_value = False

        response = client.post(
            "/movies/create",
            json={
                "tmdb_id": 123,
                "title": "Test Movie",
                "genres": ["InvalidGenre"],
                "poster_path": "/poster.jpg",
            },
        )

        assert response.status_code == 400
        assert "invalid" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_get_movie_by_id_success(self, mock_movies_dao, client, db_session, test_movie):
        mock_movies_dao.find_by_id = AsyncMock(return_value=test_movie)

        response = client.get(f"/movies/{test_movie.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_movie.id)
        assert data["tmdb_id"] == test_movie.tmdb_id

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_get_movie_by_id_not_found(self, mock_movies_dao, client, db_session):
        from uuid import uuid4
        mock_movies_dao.find_by_id = AsyncMock(return_value=None)

        response = client.get(f"/movies/{uuid4()}")

        assert response.status_code == 404
        assert "not found" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_get_movie_by_tmdb_id_success(self, mock_movies_dao, client, db_session, test_movie):
        mock_movies_dao.get_by_tmdb_id = AsyncMock(return_value=test_movie)

        response = client.get(f"/movies/by_tmdb_id/{test_movie.tmdb_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["tmdb_id"] == test_movie.tmdb_id

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_get_movie_by_tmdb_id_not_found(self, mock_movies_dao, client, db_session):
        mock_movies_dao.get_by_tmdb_id = AsyncMock(return_value=None)

        response = client.get("/movies/by_tmdb_id/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["details"]["error"].lower()

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_delete_movie_success(self, mock_movies_dao, client, db_session, test_movie):
        mock_movies_dao.find_by_id = AsyncMock(return_value=test_movie)
        mock_movies_dao.delete = AsyncMock()

        response = client.delete(f"/movies/{test_movie.id}")

        assert response.status_code == 204
        mock_movies_dao.delete.assert_called_once()

    @pytest.mark.unit
    @patch("app.controllers.movies.MoviesDAO")
    def test_delete_movie_not_found(self, mock_movies_dao, client, db_session):
        from uuid import uuid4
        mock_movies_dao.find_by_id = AsyncMock(return_value=None)

        response = client.delete(f"/movies/{uuid4()}")

        assert response.status_code == 404
        assert "not found" in response.json()["details"]["error"].lower()

