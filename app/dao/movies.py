from app.dao.base import BaseDAO
from app.db.models import Movie


class MoviesDAO(BaseDAO):
    model = Movie
