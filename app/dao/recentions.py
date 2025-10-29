from uuid import UUID

from sqlalchemy import select
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

