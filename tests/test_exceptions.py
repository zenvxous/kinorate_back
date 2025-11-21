import pytest

from app.exceptions.api import (
    EmailIsTooLong,
    Forbidden,
    InvalidCredentials,
    InvalidEmail,
    InvalidMovieStatus,
    InvalidNickname,
    InvalidRate,
    MovieNotFound,
    RecentionNotFound,
    Unauthorized,
    UserAlreadyExists,
    UserDoesntExists,
)
from app.exceptions.base import AppException


class TestExceptions:
    @pytest.mark.unit
    def test_app_exception_base(self):
        exc = AppException("Test message", "TEST_CODE", 400, {"error": "test"})

        assert exc.message == "Test message"
        assert exc.code == "TEST_CODE"
        assert exc.status_code == 400
        assert exc.details == {"error": "test"}

        result = exc.to_dict()
        assert result["message"] == "Test message"
        assert result["code"] == "TEST_CODE"
        assert result["status_code"] == 400
        assert result["details"] == {"error": "test"}

    @pytest.mark.unit
    def test_invalid_email(self):
        exc = InvalidEmail()
        assert exc.status_code == 400
        assert exc.code == "BAD_REQUEST"
        assert "email" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_user_already_exists(self):
        exc = UserAlreadyExists()
        assert exc.status_code == 400
        assert "already exists" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_invalid_credentials(self):
        exc = InvalidCredentials()
        assert exc.status_code == 400
        assert "invalid" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_unauthorized(self):
        exc = Unauthorized()
        assert exc.status_code == 401
        assert exc.code == "UNAUTHORIZED"

    @pytest.mark.unit
    def test_user_doesnt_exists(self):
        exc = UserDoesntExists()
        assert exc.status_code == 404
        assert exc.code == "NOT_FOUND"

    @pytest.mark.unit
    def test_forbidden(self):
        exc = Forbidden()
        assert exc.status_code == 403
        assert exc.code == "FORBIDDEN"

    @pytest.mark.unit
    def test_movie_not_found(self):
        exc = MovieNotFound()
        assert exc.status_code == 404
        assert "not found" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_recention_not_found(self):
        exc = RecentionNotFound()
        assert exc.status_code == 404
        assert "not found" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_invalid_rate(self):
        exc = InvalidRate()
        assert exc.status_code == 400
        assert "rate" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_invalid_movie_status(self):
        exc = InvalidMovieStatus()
        assert exc.status_code == 400
        assert "status" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_invalid_nickname(self):
        exc = InvalidNickname()
        assert exc.status_code == 400
        assert "nickname" in exc.details["error"].lower()

    @pytest.mark.unit
    def test_email_is_too_long(self):
        exc = EmailIsTooLong()
        assert exc.status_code == 400
        assert "email" in exc.details["error"].lower()

