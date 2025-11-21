from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.utils.tmdb import (
    get_genres,
    get_movie_by_tmdb_id,
    get_movie_poster,
    serch_movies,
)


class TestTMDBUtils:
    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.tmdb.ClientSession")
    @patch("app.utils.tmdb.settings")
    async def test_serch_movies(self, mock_settings, mock_client_session):
        mock_settings.TMDB_API_KEY = "test_api_key"

        mock_response_data = {
            "results": [{"id": 1, "title": "Test Movie"}],
            "page": 1,
        }

        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_client_session.return_value = mock_session

        result = await serch_movies("Test", page=1)
        assert result == mock_response_data
        mock_session.get.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.tmdb.ClientSession")
    @patch("app.utils.tmdb.settings")
    async def test_get_movie_by_tmdb_id(self, mock_settings, mock_client_session):
        mock_settings.TMDB_API_KEY = "test_api_key"

        mock_response_data = {
            "id": 123,
            "title": "Test Movie",
            "overview": "Test overview",
        }

        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_client_session.return_value = mock_session

        result = await get_movie_by_tmdb_id(123)
        assert result == mock_response_data
        mock_session.get.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.tmdb.ClientSession")
    async def test_get_movie_poster(self, mock_client_session):
        mock_image_data = b"fake_image_data"

        mock_response = MagicMock()
        mock_response.read = AsyncMock(return_value=mock_image_data)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_client_session.return_value = mock_session

        result = await get_movie_poster("/poster.jpg")
        assert result == mock_image_data
        mock_session.get.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.tmdb.ClientSession")
    @patch("app.utils.tmdb.settings")
    async def test_get_genres(self, mock_settings, mock_client_session):
        mock_settings.TMDB_API_KEY = "test_api_key"

        mock_response_data = {
            "genres": [
                {"id": 1, "name": "Action"},
                {"id": 2, "name": "Drama"},
            ]
        }

        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_client_session.return_value = mock_session

        result = await get_genres()
        assert result == mock_response_data["genres"]
        mock_session.get.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.tmdb.ClientSession")
    @patch("app.utils.tmdb.settings")
    async def test_get_genres_empty(self, mock_settings, mock_client_session):
        mock_settings.TMDB_API_KEY = "test_api_key"

        mock_response_data = {}

        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value=mock_response_data)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_client_session.return_value = mock_session

        result = await get_genres()
        assert result == []

