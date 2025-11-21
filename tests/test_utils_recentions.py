import pytest

from app.exceptions.api import (
    Forbidden,
    InvalidComment,
    InvalidMovieStatus,
    InvalidRate,
    RecentionNotFound,
)
from app.utils.recentions import (
    check_comment,
    check_movie_status,
    check_rate,
    check_recention,
    get_recention,
)


class TestRecentionsUtils:
    @pytest.mark.unit
    def test_check_movie_status_valid(self):
        assert check_movie_status("watching") is True
        assert check_movie_status("planned") is True
        assert check_movie_status("watched") is True
        assert check_movie_status("delayed") is True

    @pytest.mark.unit
    def test_check_movie_status_invalid(self):
        assert check_movie_status("invalid") is False
        assert check_movie_status("") is False
        assert check_movie_status("WATCHED") is False

    @pytest.mark.unit
    def test_check_rate_valid(self):
        assert check_rate(0) is True
        assert check_rate(5) is True
        assert check_rate(10) is True

    @pytest.mark.unit
    def test_check_rate_invalid(self):
        assert check_rate(-1) is False
        assert check_rate(11) is False

    @pytest.mark.unit
    def test_check_comment_valid(self):
        assert check_comment(None) is True
        assert check_comment("Short comment") is True
        assert check_comment("a" * 2000) is True

    @pytest.mark.unit
    def test_check_comment_invalid(self):
        assert check_comment("a" * 2001) is False

    @pytest.mark.unit
    def test_check_recention_valid(self):
        try:
            check_recention("watched", 8, "Great movie!")
        except Exception:
            pytest.fail("check_recention raised an exception for valid data")

        try:
            check_recention("watched", 8, None)
        except Exception:
            pytest.fail("check_recention raised an exception for valid data with None comment")

    @pytest.mark.unit
    def test_check_recention_invalid_status(self):
        with pytest.raises(InvalidMovieStatus):
            check_recention("invalid", 8, "Comment")

    @pytest.mark.unit
    def test_check_recention_invalid_rate(self):
        with pytest.raises(InvalidRate):
            check_recention("watched", 11, "Comment")

        with pytest.raises(InvalidRate):
            check_recention("watched", -1, "Comment")

    @pytest.mark.unit
    def test_check_recention_invalid_comment(self):
        with pytest.raises(InvalidComment):
            check_recention("watched", 8, "a" * 2001)

    @pytest.mark.unit
    async def test_get_recention_success(self, db_session, test_recention, test_user):
        recention = await get_recention(
            db_session,
            test_recention.id,
            test_user.id,
        )
        assert recention is not None
        assert recention.id == test_recention.id

    @pytest.mark.unit
    async def test_get_recention_not_found(self, db_session, test_user):
        from uuid import uuid4
        non_existent_id = uuid4()
        with pytest.raises(RecentionNotFound):
            await get_recention(db_session, non_existent_id, test_user.id)

    @pytest.mark.unit
    async def test_get_recention_forbidden(self, db_session, test_recention):
        from uuid import uuid4
        other_user_id = uuid4()
        with pytest.raises(Forbidden):
            await get_recention(db_session, test_recention.id, other_user_id)

