import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.movies import MoviesDAO
from app.dao.recentions import RecentionsDAO
from app.db.models import Movie, Recention, User


class TestRecentionsDAO:
    @pytest.mark.unit
    async def test_find_all_by_user_id(self, db_session: AsyncSession, test_user: User, test_movie: Movie):
        recention1 = await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great!",
        )

        movie2 = await MoviesDAO.add(
            db_session,
            tmdb_id=12345,
            title="Another Movie",
            genres=["Comedy"],
            poster_path="/poster2.jpg",
        )
        await db_session.commit()

        recention2 = await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=movie2.id,
            rate=7,
            movie_status="watched",
            comment="Good!",
        )
        await db_session.commit()

        recentions = await RecentionsDAO.find_all_by_user_id(db_session, test_user.id)
        assert len(recentions) >= 2
        recention_ids = [r.id for r in recentions]
        assert recention1.id in recention_ids
        assert recention2.id in recention_ids

    @pytest.mark.unit
    async def test_find_all_by_user_id_empty(self, db_session: AsyncSession, test_user: User):
        recentions = await RecentionsDAO.find_all_by_user_id(db_session, test_user.id)
        assert len(recentions) == 0

    @pytest.mark.unit
    async def test_find_by_id_with_movie(self, db_session: AsyncSession, test_recention: Recention):
        found_recention = await RecentionsDAO.find_by_id(db_session, test_recention.id)
        assert found_recention is not None
        assert found_recention.id == test_recention.id
        assert found_recention.movie is not None
        assert found_recention.movie.id == test_recention.movie.id

    @pytest.mark.unit
    async def test_update_with_movie(self, db_session: AsyncSession, test_recention: Recention):
        updated_recention = await RecentionsDAO.update(
            db_session,
            id=test_recention.id,
            rate=9,
            comment="Updated comment",
        )
        await db_session.commit()

        assert updated_recention is not None
        assert updated_recention.rate == 9
        assert updated_recention.comment == "Updated comment"
        assert updated_recention.movie is not None

    @pytest.mark.unit
    async def test_get_stats_by_user_id(self, db_session: AsyncSession, test_user: User, test_movie: Movie):
        await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=8,
            movie_status="watched",
            comment="Great movie!",
        )

        movie2 = await MoviesDAO.add(
            db_session,
            tmdb_id=12346,
            title="Movie 2",
            genres=["Action"],
            poster_path="/poster3.jpg",
        )
        await db_session.commit()

        await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=movie2.id,
            rate=9,
            movie_status="watched",
            comment="Excellent!",
        )

        movie3 = await MoviesDAO.add(
            db_session,
            tmdb_id=12347,
            title="Movie 3",
            genres=["Drama"],
            poster_path="/poster4.jpg",
        )
        await db_session.commit()

        await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=movie3.id,
            rate=0,
            movie_status="planned",
            comment=None,
        )
        await db_session.commit()

        stats = await RecentionsDAO.get_stats_by_user_id(db_session, test_user.id)
        assert stats["movies_watched"] == 2
        assert stats["average_rating"] == 8.5
        assert stats["reviews_written"] == 2

    @pytest.mark.unit
    async def test_get_stats_by_user_id_no_watched(self, db_session: AsyncSession, test_user: User, test_movie: Movie):
        await RecentionsDAO.add(
            db_session,
            user_id=test_user.id,
            movie_id=test_movie.id,
            rate=0,
            movie_status="planned",
            comment=None,
        )
        await db_session.commit()

        stats = await RecentionsDAO.get_stats_by_user_id(db_session, test_user.id)
        assert stats["movies_watched"] == 0
        assert stats["average_rating"] is None
        assert stats["reviews_written"] == 0

    @pytest.mark.unit
    async def test_get_stats_by_user_id_no_recentions(self, db_session: AsyncSession, test_user: User):
        stats = await RecentionsDAO.get_stats_by_user_id(db_session, test_user.id)
        assert stats["movies_watched"] == 0
        assert stats["average_rating"] is None
        assert stats["reviews_written"] == 0

