from uuid import UUID

from pydantic import BaseModel


class MovieInRecentionResponse(BaseModel):
    id: UUID
    tmdb_id: int
    title: str
    genres: list[str]

class CreateMovieSchema(BaseModel):
    tmdb_id: int
    title: str
    genres: list[str]
    poster_path: str

class MovieResponse(BaseModel):
    id: UUID
    tmdb_id: int
    title: str
    genres: list[str]
    poster_path: str
