from fastapi import APIRouter, Response

from app.utils.tmdb import (
    get_genres,
    get_movie_by_tmdb_id,
    get_movie_poster,
    serch_movies,
)

router = APIRouter(
    prefix="/tmdb",
    tags=["tmdb"],
)

@router.get("/by_title/{title}/{page}")
async def find_movies_by_title(title: str, page: int = 1):
    return await serch_movies(title=title, page=page)

@router.get("/by_id/{tmdb_id}")
async def find_movie_by_tmdb_id(tmdb_id: int):
    return await get_movie_by_tmdb_id(movie_id=tmdb_id)

@router.get("/poster/{poster_path}")
async def get_poster(poster_path: str):
    image = await get_movie_poster(poster_path=poster_path)
    return Response(content=image, media_type="image/jpeg")

@router.get("/genres")
async def get_movie_genres():
    return await get_genres()
