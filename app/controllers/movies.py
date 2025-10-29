from fastapi import APIRouter, Depends

from app.dao.movies import MoviesDAO
from app.db.config import get_db
from app.exceptions.api import MovieAlreadyExists
from app.schemas.movies import CreateMovieSchema, MovieResponse

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.post("/create")
async def create_movie(
    data: CreateMovieSchema,
    session = Depends(get_db)
):
    if await MoviesDAO.get_by_tmdb_id(session=session, tmdb_id=data.tmdb_id):
        raise MovieAlreadyExists

    movie = await MoviesDAO.add(
        session=session,
        tmdb_id=data.tmdb_id,
        title=data.title,
        genres=data.genres,
        poster_path=data.poster_path,
    )
    await session.commit()

    return MovieResponse(
        id=movie.id,
        tmdb_id=movie.tmdb_id,
        title=movie.title,
        genres=movie.genres,
        poster_path=movie.poster_path,
    )

@router.get("/{movie_id}")
async def get_movie_by_id(
    movie_id: str,
    session = Depends(get_db)
):
    movie = await MoviesDAO.find_by_id(session=session, model_id=movie_id)
    return MovieResponse(
        id=movie.id,
        tmdb_id=movie.tmdb_id,
        title=movie.title,
        genres=movie.genres,
        poster_path=movie.poster_path,
    )
