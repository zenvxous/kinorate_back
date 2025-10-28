from aiohttp import ClientSession

from app.settings import settings


async def serch_movies(title: str, page: int = 1):
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US&page={page}"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + settings.TMDB_API_KEY,
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def get_movie_by_tmdb_id(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + settings.TMDB_API_KEY,
    }

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()
