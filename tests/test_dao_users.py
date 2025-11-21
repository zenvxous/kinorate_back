import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.users import UsersDAO
from app.db.models import User


class TestUsersDAO:
    @pytest.mark.unit
    async def test_get_by_email(self, db_session: AsyncSession, test_user: User):
        found_user = await UsersDAO.get_by_email(db_session, test_user.email)
        assert found_user is not None
        assert found_user.email == test_user.email
        assert found_user.id == test_user.id

    @pytest.mark.unit
    async def test_get_by_email_not_found(self, db_session: AsyncSession):
        found_user = await UsersDAO.get_by_email(db_session, "nonexistent@example.com")
        assert found_user is None

    @pytest.mark.unit
    async def test_get_by_email_or_nickname_by_email(self, db_session: AsyncSession, test_user: User):
        users = await UsersDAO.get_by_email_or_nickname(
            db_session,
            email=test_user.email,
            nickname="different_nickname",
        )
        assert len(users) == 1
        assert users[0].email == test_user.email

    @pytest.mark.unit
    async def test_get_by_email_or_nickname_by_nickname(self, db_session: AsyncSession, test_user: User):
        users = await UsersDAO.get_by_email_or_nickname(
            db_session,
            email="different@example.com",
            nickname=test_user.nickname,
        )
        assert len(users) == 1
        assert users[0].nickname == test_user.nickname

    @pytest.mark.unit
    async def test_get_by_email_or_nickname_both_match(self, db_session: AsyncSession, test_user: User):
        users = await UsersDAO.get_by_email_or_nickname(
            db_session,
            email=test_user.email,
            nickname=test_user.nickname,
        )
        assert len(users) == 1
        assert users[0].id == test_user.id

    @pytest.mark.unit
    async def test_get_by_email_or_nickname_no_match(self, db_session: AsyncSession):
        users = await UsersDAO.get_by_email_or_nickname(
            db_session,
            email="nonexistent@example.com",
            nickname="nonexistent",
        )
        assert len(users) == 0

    @pytest.mark.unit
    async def test_get_by_email_or_nickname_multiple_users(self, db_session: AsyncSession):
        user1 = await UsersDAO.add(
            db_session,
            email="user1@example.com",
            nickname="user1",
            password_hash="hash1",
        )
        user2 = await UsersDAO.add(
            db_session,
            email="user2@example.com",
            nickname="user2",
            password_hash="hash2",
        )
        await db_session.commit()

        users = await UsersDAO.get_by_email_or_nickname(
            db_session,
            email=user1.email,
            nickname=user2.nickname,
        )
        assert len(users) == 2
        user_ids = [user.id for user in users]
        assert user1.id in user_ids
        assert user2.id in user_ids

