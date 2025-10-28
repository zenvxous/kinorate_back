from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.db.models import User


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def get_by_email_or_nickname(cls, session: AsyncSession, email: str, nickname: str) -> list[User]:
        query = select(cls.model).where(
            (cls.model.email == email) | (cls.model.nickname == nickname)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> User | None:
        return await cls.find_one_or_none(session=session, email=email)
