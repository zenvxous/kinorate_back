from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Recention
from app.exceptions.api import (
    InvalidComment,
    InvalidMovieStatus,
    InvalidRate,
)


def check_movie_status(status: str) -> bool:
    valid_statuses = {"watching", "planned", "watched", "delayed"}
    return status in valid_statuses

def check_rate(rate: int) -> bool:
    return 0 <= rate <= 10

def check_comment(comment: str | None) -> bool:
    if comment is None:
        return True
    return len(comment) <= 2000

def check_recention(status: str, rate: int, comment: str | None):
    if not check_movie_status(status):
        raise InvalidMovieStatus
    if not check_rate(rate):
        raise InvalidRate
    if not check_comment(comment):
        raise InvalidComment

async def get_recention(
        session: AsyncSession,
        recention_id: UUID,
        user_id: UUID,
) -> Recention:
    from app.dao.recentions import RecentionsDAO
    from app.exceptions.api import Forbidden, RecentionNotFound

    recention = await RecentionsDAO.find_by_id(session=session, id=recention_id)
    if not recention:
        raise RecentionNotFound
    if recention.user_id != user_id:
        raise Forbidden
    return recention
