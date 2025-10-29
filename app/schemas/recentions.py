from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.movies import MovieInRecentionResponse


class RecentionSmallResponse(BaseModel):
    id: UUID
    rate: int
    movie_status: str

    movie: MovieInRecentionResponse

    model_config = ConfigDict(from_attributes=True)
