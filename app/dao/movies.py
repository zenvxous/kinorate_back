from app.dao.base import BaseDAO
from app.db.models import Movie


class MoviesDAO(BaseDAO):
    model = Movie

    @classmethod
    async def get_by_tmdb_id(cls, session, tmdb_id: int) -> Movie | None:
        return await cls.find_one_or_none(session=session, tmdb_id=tmdb_id)
