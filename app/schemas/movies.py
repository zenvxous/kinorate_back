from uuid import UUID

from pydantic import BaseModel


class MovieInRecintionResponse(BaseModel):
    id: UUID
    tmdb_id: int
    title: str
    genres: list[str]
