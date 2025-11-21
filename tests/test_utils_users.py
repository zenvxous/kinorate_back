import pytest

from app.exceptions.api import (
    EmailIsTooLong,
    InvalidEmail,
    InvalidNickname,
)
from app.utils.users import (
    check_email_length,
    check_nickname,
    check_user,
    is_valid_email,
)


class TestUsersUtils:
    @pytest.mark.unit
    def test_is_valid_email_valid(self):
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("user.name@domain.co.uk") is True
        assert is_valid_email("user+tag@example.com") is True

    @pytest.mark.unit
    def test_is_valid_email_invalid(self):
        assert is_valid_email("invalid") is False
        assert is_valid_email("invalid@") is False
        assert is_valid_email("invalid@example") is False
        assert is_valid_email("") is False

    @pytest.mark.unit
    def test_check_email_length_valid(self):
        assert check_email_length("test@example.com") is True
        assert check_email_length("a" * 256) is True

    @pytest.mark.unit
    def test_check_email_length_invalid(self):
        assert check_email_length("a" * 257) is False

    @pytest.mark.unit
    def test_check_nickname_valid(self):
        assert check_nickname("user123") is True
        assert check_nickname("abc") is True
        assert check_nickname("a" * 50) is True
        assert check_nickname("User123") is True

    @pytest.mark.unit
    def test_check_nickname_invalid(self):
        assert check_nickname("ab") is False
        assert check_nickname("a" * 51) is False
        assert check_nickname("user name") is False
        assert check_nickname("user-name") is False
        assert check_nickname("user_name") is False
        assert check_nickname("") is False

    @pytest.mark.unit
    def test_check_user_valid(self):
        try:
            check_user("test@example.com", "user123")
        except Exception:
            pytest.fail("check_user raised an exception for valid data")

    @pytest.mark.unit
    def test_check_user_invalid_email(self):
        with pytest.raises(InvalidEmail):
            check_user("invalid-email", "user123")

    @pytest.mark.unit
    def test_check_user_email_too_long(self):
        long_email = "a" * 257 + "@example.com"
        with pytest.raises(EmailIsTooLong):
            check_user(long_email, "user123")

    @pytest.mark.unit
    def test_check_user_invalid_nickname(self):
        with pytest.raises(InvalidNickname):
            check_user("test@example.com", "ab")

        with pytest.raises(InvalidNickname):
            check_user("test@example.com", "user name")

