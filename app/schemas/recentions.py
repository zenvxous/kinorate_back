from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.movies import MovieInRecentionResponse, MovieInRecentionSmallResponse


class RecentionSmallResponse(BaseModel):
    id: UUID
    rate: int
    movie_status: str

    movie: MovieInRecentionSmallResponse

    model_config = ConfigDict(from_attributes=True)

class CreateRecentionSchema(BaseModel):
    rate: int
    movie_status: str
    comment: str | None = None

    movie_id: UUID

class UpdateRecentionSchema(BaseModel):
    rate: int
    movie_status: str
    comment: str | None = None

class RecentionResponse(BaseModel):
    id: UUID
    rate: int
    movie_status: str
    comment: str | None = None

    movie: MovieInRecentionResponse

    model_config = ConfigDict(from_attributes=True)
