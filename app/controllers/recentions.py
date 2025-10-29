from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.movies import MoviesDAO
from app.dao.recentions import RecentionsDAO
from app.db.config import get_db
from app.exceptions.api import MovieNotFound
from app.schemas.recentions import (
    CreateRecentionSchema,
    RecentionResponse,
    RecentionSmallResponse,
    UpdateRecentionSchema,
)
from app.utils.recentions import check_recention, get_recention
from app.utils.session import required_user

router = APIRouter(
    prefix="/recentions",
    tags=["recentions"],
)

@router.get("/users/me")
async def get_recentions_by_me(
    user = Depends(required_user),
    session: AsyncSession = Depends(get_db),
) -> list[RecentionSmallResponse]:

    recentions = await RecentionsDAO.find_all_by_user_id(session=session, user_id=user.id)
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
    session: AsyncSession = Depends(get_db),
) -> RecentionResponse:
    recention = await get_recention(session=session, recention_id=recention_id, user_id=user.id)

    return RecentionResponse(
        id=recention.id,
        rate=recention.rate,
        movie_status=recention.movie_status,
        comment=recention.comment,
        movie={
            "id": recention.movie.id,
            "title": recention.movie.title,
            "tmdb_id": recention.movie.tmdb_id,
            "genres": recention.movie.genres,
            "poster_path": recention.movie.poster_path,
        })

@router.post("/create", status_code=201)
async def create_recention(
    data: CreateRecentionSchema,
    user = Depends(required_user),
    session: AsyncSession = Depends(get_db)
) -> RecentionResponse:
    check_recention(status=data.movie_status, rate=data.rate, comment=data.comment)

    if not await MoviesDAO.find_by_id(session=session, model_id=data.movie_id):
        raise MovieNotFound

    recention = await RecentionsDAO.add(
        session=session,
        user_id=user.id,
        movie_id=data.movie_id,
        rate=data.rate,
        movie_status=data.movie_status,
        comment=data.comment,
    )
    await session.commit()

    recention = await get_recention(session=session, recention_id=recention.id, user_id=user.id)

    return RecentionResponse(
        id=recention.id,
        rate=recention.rate,
        movie_status=recention.movie_status,
        comment=recention.comment,
        movie={
            "id": recention.movie.id,
            "title": recention.movie.title,
            "tmdb_id": recention.movie.tmdb_id,
            "genres": recention.movie.genres,
            "poster_path": recention.movie.poster_path,
        })

@router.put("/{recention_id}")
async def update_recention(
    recention_id: UUID,
    data: UpdateRecentionSchema,
    user = Depends(required_user),
    session: AsyncSession = Depends(get_db)
) -> RecentionResponse:
    await get_recention(session=session, recention_id=recention_id, user_id=user.id)

    check_recention(status=data.movie_status, rate=data.rate, comment=data.comment)

    updated_recention = await RecentionsDAO.update(
        session=session,
        id=recention_id,
        rate=data.rate,
        movie_status=data.movie_status,
        comment=data.comment,
    )
    await session.commit()
    return RecentionResponse(
        id=updated_recention.id,
        rate=updated_recention.rate,
        movie_status=updated_recention.movie_status,
        comment=updated_recention.comment,
        movie={
            "id": updated_recention.movie.id,
            "title": updated_recention.movie.title,
            "tmdb_id": updated_recention.movie.tmdb_id,
            "genres": updated_recention.movie.genres,
            "poster_path": updated_recention.movie.poster_path,
        })

@router.delete("/{recention_id}", status_code=204)
async def delete_recention(
    recention_id: UUID,
    user = Depends(required_user),
    session: AsyncSession = Depends(get_db)
):
    await get_recention(session=session, recention_id=recention_id, user_id=user.id)

    await RecentionsDAO.delete(session=session, id=recention_id)
    await session.commit()
