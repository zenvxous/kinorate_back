from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers.tmdb import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestTMDBController:
    @pytest.mark.unit
    @patch("app.controllers.tmdb.serch_movies")
    def test_find_movies_by_title(self, mock_serch_movies, client):
        """Test finding movies by title."""
        mock_serch_movies.return_value = {
            "results": [{"id": 1, "title": "Test Movie"}],
            "page": 1,
        }

        response = client.get("/tmdb/by_title/Test/1")

        assert response.status_code == 200
        mock_serch_movies.assert_called_once_with(title="Test", page=1)

    @pytest.mark.unit
    @patch("app.controllers.tmdb.get_movie_by_tmdb_id")
    def test_find_movie_by_tmdb_id(self, mock_get_movie, client):
        mock_get_movie.return_value = {
            "id": 123,
            "title": "Test Movie",
            "overview": "Test overview",
        }

        response = client.get("/tmdb/by_id/123")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 123
        mock_get_movie.assert_called_once_with(movie_id=123)

    @pytest.mark.unit
    @patch("app.controllers.tmdb.get_movie_poster")
    def test_get_poster(self, mock_get_poster, client):
        mock_image_data = b"fake_image_data"
        mock_get_poster.return_value = mock_image_data

        response = client.get("/tmdb/poster/poster.jpg")

        assert response.status_code == 200
        assert response.content == mock_image_data
        assert response.headers["content-type"] == "image/jpeg"
        mock_get_poster.assert_called_once_with(poster_path="poster.jpg")

    @pytest.mark.unit
    @patch("app.controllers.tmdb.get_genres")
    def test_get_movie_genres(self, mock_get_genres, client):
        mock_get_genres.return_value = [
            {"id": 1, "name": "Action"},
            {"id": 2, "name": "Drama"},
        ]

        response = client.get("/tmdb/genres")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Action"
        mock_get_genres.assert_called_once()

