from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Movie, User, generate_uuid


class TestModels:
    @pytest.mark.unit
    def test_generate_uuid(self):
        uuid = generate_uuid()
        assert isinstance(uuid, UUID)

        uuid1 = generate_uuid()
        uuid2 = generate_uuid()
        assert uuid1 != uuid2

    @pytest.mark.unit
    async def test_user_model(self, db_session: AsyncSession):
        from app.dao.users import UsersDAO

        user = await UsersDAO.add(
            db_session,
            email="test@example.com",
            nickname="testuser",
            password_hash="hashed_password",
        )
        await db_session.commit()

        assert user.id is not None
        assert isinstance(user.id, UUID)
        assert user.email == "test@example.com"
        assert user.nickname == "testuser"
        assert user.password_hash == "hashed_password"
        assert user.created_at is not None

    @pytest.mark.unit
    async def test_movie_model(self, db_session: AsyncSession):
        from app.dao.movies import MoviesDAO

        movie = await MoviesDAO.add(
            db_session,
            tmdb_id=123,
            title="Test Movie",
            genres=["Action", "Drama"],
            poster_path="/poster.jpg",
        )
        await db_session.commit()

        assert movie.id is not None
        assert isinstance(movie.id, UUID)
        assert movie.tmdb_id == 123
        assert movie.title == "Test Movie"
        assert movie.genres == ["Action", "Drama"]
        assert movie.poster_path == "/poster.jpg"
        assert movie.created_at is not None

    @pytest.mark.unit
    async def test_recention_model(self, db_session: AsyncSession, test_user: User, test_movie: Movie):
        from app.dao.recentions import RecentionsDAO

        recention = await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great movie!",
        )
        await db_session.commit()

        assert recention.id is not None
        assert isinstance(recention.id, UUID)
        assert recention.user_id == test_user.id
        assert recention.movie_id == test_movie.id
        assert recention.rate == 8
        assert recention.movie_status == "watched"
        assert recention.comment == "Great movie!"
        assert recention.created_at is not None

    @pytest.mark.unit
    async def test_user_recentions_relationship(self, db_session: AsyncSession, test_user: User, test_movie: Movie):
        from app.dao.recentions import RecentionsDAO

        await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great!",
        )
        await db_session.commit()
        await db_session.refresh(test_user)

    @pytest.mark.unit
    async def test_movie_recentions_relationship(self, db_session: AsyncSession, test_user: User, test_movie: Movie):
        from app.dao.recentions import RecentionsDAO

        await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great!",
        )
        await db_session.commit()
