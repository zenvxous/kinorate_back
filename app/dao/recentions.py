from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.db.models import Recention


class RecentionsDAO(BaseDAO):
    model = Recention

    @classmethod
    async def find_all_by_user_id(cls, session: AsyncSession, user_id: UUID) -> list[Recention]:
        query = select(cls.model).where(cls.model.user_id == user_id).options(selectinload(cls.model.movie))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(cls, session, id, **data) -> Recention:
        await super().update(session, id, **data)
        query = select(cls.model).where(cls.model.id == id).options(selectinload(cls.model.movie))
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def find_by_id(cls, session, id) -> Recention:
        query = select(cls.model).where(cls.model.id == id).options(selectinload(cls.model.movie))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_stats_by_user_id(cls, session: AsyncSession, user_id: UUID) -> dict:
        stmt = (
            select(
                func.count(case((Recention.movie_status == "watched", 1))).label("movies_watched"),
                func.avg(case((Recention.rate > 0, Recention.rate))).label("average_rating"),
                func.count(Recention.comment).label("reviews_written"),
            )
            .filter_by(user_id=user_id)
        )
        result = await session.execute(stmt)
        stats = result.mappings().one_or_none()

        if not stats or stats["movies_watched"] == 0:
            return {
                "movies_watched": 0,
                "average_rating": None,
                "reviews_written": 0,
            }

        movies_watched = stats.get("movies_watched", 0)
        avg_rating_raw = stats.get("average_rating")
        reviews_written = stats.get("reviews_written", 0)

        avg_rating = float(avg_rating_raw) if avg_rating_raw is not None else None

        return {
            "movies_watched": movies_watched,
            "average_rating": round(avg_rating, 1) if avg_rating is not None else None,
            "reviews_written": reviews_written,
        }
