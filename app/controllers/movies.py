from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.movies import MoviesDAO
from app.db.config import get_db
from app.exceptions.api import (
    InvalidMovieGenres,
    MovieAlreadyExists,
    MovieNotFound,
)
from app.schemas.movies import CreateMovieSchema, MovieResponse
from app.utils.movies import check_genres

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.post("/create", status_code=201)
async def create_movie(
    data: CreateMovieSchema,
    session: AsyncSession = Depends(get_db)
) -> MovieResponse:
    if await MoviesDAO.get_by_tmdb_id(session=session, tmdb_id=data.tmdb_id):
        raise MovieAlreadyExists
    if not check_genres(data.genres):
        raise InvalidMovieGenres

    movie = await MoviesDAO.add(
        session=session,
        tmdb_id=data.tmdb_id,
        title=data.title,
        genres=data.genres.sort(),
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
    session: AsyncSession = Depends(get_db)
) -> MovieResponse:
    movie = await MoviesDAO.find_by_id(session=session, model_id=movie_id)
    if not movie:
        raise MovieNotFound

    return MovieResponse(
        id=movie.id,
        tmdb_id=movie.tmdb_id,
        title=movie.title,
        genres=movie.genres,
        poster_path=movie.poster_path,
    )

@router.get("/by_tmdb_id/{tmdb_id}")
async def get_movie_by_tmdb_id(
    tmdb_id: int,
    session: AsyncSession = Depends(get_db)
) -> MovieResponse:
    movie = await MoviesDAO.get_by_tmdb_id(session=session, tmdb_id=tmdb_id)
    if not movie:
        raise MovieNotFound

    return MovieResponse(
        id=movie.id,
        tmdb_id=movie.tmdb_id,
        title=movie.title,
        genres=movie.genres,
        poster_path=movie.poster_path,
    )
