from fastapi import APIRouter

from app.utils.tmdb import (
    get_movie_by_tmdb_id,
    serch_movies,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.get("/find_by_title/{title}/{page}")
async def find_movies_by_title(title: str, page: int = 1):
    return await serch_movies(title=title, page=page)

@router.get("/find_by_tmdb_id/{tmdb_id}")
async def find_movie_by_tmdb_id(tmdb_id: int):
    return await get_movie_by_tmdb_id(movie_id=tmdb_id)


