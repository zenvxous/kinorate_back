from uuid import UUID

from fastapi import APIRouter, Depends

from app.dao.recentions import RecentionsDAO
from app.db.config import get_db
from app.exceptions.api import Forbidden
from app.schemas.recentions import RecentionSmallResponse
from app.utils.session import required_user

router = APIRouter(
    prefix="/recentions",
    tags=["recentions"],
)

@router.get("/user/{user_id}")
async def get_recentions_by_user(
    user_id: UUID,
    user = Depends(required_user),
    session = Depends(get_db),
) -> list[RecentionSmallResponse]:
    if user.id != user_id:
        raise Forbidden

    recentions = await RecentionsDAO.find_all_by_user_id(session=session, user_id=user_id)
    responses = []
    for recention in recentions:
        responses.append(
            RecentionSmallResponse(
                id=recention.id,
                rate=recention.rate,
                movie_status=recention.movie_status,
                movie={
                    "id": recention.movie.id,
                    "title": recention.movie.title,
                    "tmdb_id": recention.movie.tmdb_id,
                    "genres": recention.movie.genres,
                }
            )
        )
    return responses

@router.get("/{recention_id}")
async def get_recention_by_id(
    recention_id: UUID,
    user = Depends(required_user),
    session = Depends(get_db),
):
    recention = await RecentionsDAO.find_by_id(session=session, model_id=recention_id)
    if recention.user_id != user.id:
        raise Forbidden

    return recention
