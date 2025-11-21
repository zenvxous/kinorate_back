import asyncio
import json
from collections.abc import AsyncGenerator

import pytest
from faker import Faker
from sqlalchemy import ARRAY, String, TypeDecorator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.dao.movies import MoviesDAO
from app.dao.recentions import RecentionsDAO
from app.dao.users import UsersDAO
from app.db.models import Base, Movie, Recention, User

fake = Faker()


class JSONType(TypeDecorator):
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(String)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


def patch_models_for_sqlite():
    for table in Base.metadata.tables.values():
        for column in table.columns:
            if isinstance(column.type, ARRAY):
                column.type = JSONType()


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

patch_models_for_sqlite()

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    patch_models_for_sqlite()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = await UsersDAO.add(
        db_session,
        email=fake.email(),
        nickname=fake.user_name()[:50],
        password_hash="hashed_password",
    )
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_movie(db_session: AsyncSession) -> Movie:
    movie = await MoviesDAO.add(
        db_session,
        tmdb_id=fake.random_int(min=1, max=1000000),
        title=fake.sentence(nb_words=3)[:256],
        genres=["Action", "Drama"],
        poster_path="/test_poster.jpg",
    )
    await db_session.commit()
    await db_session.refresh(movie)
    return movie


@pytest.fixture
async def test_recention(db_session: AsyncSession, test_user: User, test_movie: Movie) -> Recention:
    recention = await RecentionsDAO.add(
        db_session,
        user_id=test_user.id,
        movie_id=test_movie.id,
        rate=8,
        movie_status="watched",
        comment="Great movie!",
    )
    await db_session.commit()
    await db_session.refresh(recention)
    return recention


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    async def _get_db():
        yield db_session
    return _get_db

