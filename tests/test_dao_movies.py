import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.movies import MoviesDAO
from app.db.models import Movie


class TestMoviesDAO:
    @pytest.mark.unit
    async def test_get_by_tmdb_id(self, db_session: AsyncSession, test_movie: Movie):
        found_movie = await MoviesDAO.get_by_tmdb_id(db_session, test_movie.tmdb_id)
        assert found_movie is not None
        assert found_movie.tmdb_id == test_movie.tmdb_id
        assert found_movie.id == test_movie.id

    @pytest.mark.unit
    async def test_get_by_tmdb_id_not_found(self, db_session: AsyncSession):
        found_movie = await MoviesDAO.get_by_tmdb_id(db_session, 999999)
        assert found_movie is None

