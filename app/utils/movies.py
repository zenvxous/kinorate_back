from app.utils.tmdb import get_genres

_cached_valid_genres: set[str] | None = None

async def check_genres(genres: list[str]) -> bool:
    global _cached_valid_genres

    if _cached_valid_genres is None:
        tmdb_genres_list = await get_genres()
        _cached_valid_genres = {genre['name'] for genre in tmdb_genres_list}

    return all(genre in _cached_valid_genres for genre in genres)
