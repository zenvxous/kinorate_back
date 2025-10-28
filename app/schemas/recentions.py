from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.movies import MovieInRecintionResponse


class RecentionSmallResponse(BaseModel):
    id: UUID
    rate: int
    movie_status: str

    movie: MovieInRecintionResponse

    model_config = ConfigDict(from_attributes=True)
