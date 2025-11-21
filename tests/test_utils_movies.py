from unittest.mock import patch

import pytest

from app.utils.movies import check_genres


class TestMoviesUtils:
    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.movies.get_genres")
    async def test_check_genres_valid(self, mock_get_genres):
        mock_get_genres.return_value = [
            {"name": "Action"},
            {"name": "Drama"},
            {"name": "Comedy"},
        ]

        result = await check_genres(["Action", "Drama"])
        assert result is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.movies.get_genres")
    async def test_check_genres_invalid(self, mock_get_genres):
        mock_get_genres.return_value = [
            {"name": "Action"},
            {"name": "Drama"},
            {"name": "Comedy"},
        ]

        result = await check_genres(["Action", "InvalidGenre"])
        assert result is False

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.movies.get_genres")
    async def test_check_genres_cached(self, mock_get_genres):
        import app.utils.movies as movies_module
        movies_module._cached_valid_genres = None

        mock_get_genres.return_value = [
            {"name": "Action"},
            {"name": "Drama"},
        ]

        await check_genres(["Action"])
        assert mock_get_genres.call_count == 1

        await check_genres(["Drama"])
        assert mock_get_genres.call_count == 1

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.movies.get_genres")
    async def test_check_genres_empty_list(self, mock_get_genres):
        mock_get_genres.return_value = [
            {"name": "Action"},
            {"name": "Drama"},
        ]

        result = await check_genres([])
        assert result is True

