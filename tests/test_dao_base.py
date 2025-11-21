from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.users import UsersDAO
from app.db.models import User


class TestBaseDAO:
    @pytest.mark.unit
    async def test_find_by_id(self, db_session: AsyncSession, test_user: User):
        found_user = await UsersDAO.find_by_id(db_session, test_user.id)
        assert found_user is not None
        assert found_user.id == test_user.id
        assert found_user.email == test_user.email

    @pytest.mark.unit
    async def test_find_by_id_not_found(self, db_session: AsyncSession):
        non_existent_id = uuid4()
        found_user = await UsersDAO.find_by_id(db_session, non_existent_id)
        assert found_user is None

    @pytest.mark.unit
    async def test_find_one_or_none(self, db_session: AsyncSession, test_user: User):
        found_user = await UsersDAO.find_one_or_none(db_session, email=test_user.email)
        assert found_user is not None
        assert found_user.email == test_user.email

    @pytest.mark.unit
    async def test_find_one_or_none_not_found(self, db_session: AsyncSession):
        found_user = await UsersDAO.find_one_or_none(db_session, email="nonexistent@example.com")
        assert found_user is None

    @pytest.mark.unit
    async def test_find_all(self, db_session: AsyncSession):
        await UsersDAO.add(
            db_session,
            email="user1@example.com",
            nickname="user1",
            password_hash="hash1",
        )
        await UsersDAO.add(
            db_session,
            email="user2@example.com",
            nickname="user2",
            password_hash="hash2",
        )
        await db_session.commit()

        users = await UsersDAO.find_all(db_session)
        assert len(users) >= 2
        emails = [user.email for user in users]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    @pytest.mark.unit
    async def test_find_all_with_limit(self, db_session: AsyncSession):
        for i in range(5):
            await UsersDAO.add(
                db_session,
                email=f"user{i}@example.com",
                nickname=f"user{i}",
                password_hash=f"hash{i}",
            )
        await db_session.commit()

        users = await UsersDAO.find_all(db_session, limit=3)
        assert len(users) == 3

    @pytest.mark.unit
    async def test_find_all_with_offset(self, db_session: AsyncSession):
        for i in range(5):
            await UsersDAO.add(
                db_session,
                email=f"user{i}@example.com",
                nickname=f"user{i}",
                password_hash=f"hash{i}",
            )
        await db_session.commit()

        all_users = await UsersDAO.find_all(db_session)
        offset_users = await UsersDAO.find_all(db_session, offset=2)
        assert len(offset_users) == len(all_users) - 2

    @pytest.mark.unit
    async def test_add(self, db_session: AsyncSession):
        user = await UsersDAO.add(
            db_session,
            email="newuser@example.com",
            nickname="newuser",
            password_hash="hashed_password",
        )
        await db_session.commit()

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.nickname == "newuser"

    @pytest.mark.unit
    async def test_update(self, db_session: AsyncSession, test_user: User):
        updated_user = await UsersDAO.update(
            db_session,
            id=test_user.id,
            nickname="updated_nickname",
        )
        await db_session.commit()
        await db_session.refresh(updated_user)

        assert updated_user.nickname == "updated_nickname"
        assert updated_user.email == test_user.email

    @pytest.mark.unit
    async def test_delete(self, db_session: AsyncSession, test_user: User):
        user_id = test_user.id
        await UsersDAO.delete(db_session, id=user_id)
        await db_session.commit()

        deleted_user = await UsersDAO.find_by_id(db_session, user_id)
        assert deleted_user is None

    @pytest.mark.unit
    async def test_count(self, db_session: AsyncSession):
        initial_count = await UsersDAO.count(db_session)

        await UsersDAO.add(
            db_session,
            email="countuser@example.com",
            nickname="countuser",
            password_hash="hash",
        )
        await db_session.commit()

        new_count = await UsersDAO.count(db_session)
        assert new_count == initial_count + 1

    @pytest.mark.unit
    async def test_exists(self, db_session: AsyncSession, test_user: User):
        exists = await UsersDAO.exists(db_session, email=test_user.email)
        assert exists is True

        exists = await UsersDAO.exists(db_session, email="nonexistent@example.com")
        assert exists is False

