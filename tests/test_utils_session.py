from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from app.exceptions.api import Unauthorized, UserDoesntExists
from app.utils.session import (
    add_users_response_cookie,
    hash_password,
    required_user,
    verify_password,
)


class TestSessionUtils:
    @pytest.mark.unit
    def test_hash_password(self):
        password = "test_password"
        hashed = hash_password(password)

        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    @pytest.mark.unit
    def test_verify_password_correct(self):
        password = "test_password"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    @pytest.mark.unit
    def test_verify_password_incorrect(self):
        password = "test_password"
        hashed = hash_password(password)

        assert verify_password("wrong_password", hashed) is False

    @pytest.mark.unit
    def test_hash_password_different_hashes(self):
        password = "test_password"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)

        assert hashed1 != hashed2
        assert verify_password(password, hashed1) is True
        assert verify_password(password, hashed2) is True

    @pytest.mark.unit
    @patch("app.utils.session.settings")
    def test_add_users_response_cookie(self, mock_settings):
        from unittest.mock import MagicMock

        from fastapi import Response

        mock_security = MagicMock()
        mock_token = "test_token"
        mock_settings.security = mock_security
        mock_settings.JWT_EXPIRY_USER_SECONDS = 3600

        mock_security.create_access_token.return_value = mock_token
        mock_security.set_access_cookies = MagicMock()

        response = Response()
        add_users_response_cookie(response, "user_id_123")

        mock_security.create_access_token.assert_called_once()
        mock_security.set_access_cookies.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.session.async_session")
    @patch("app.utils.session.settings")
    @patch("app.utils.session.UsersDAO")
    async def test_required_user_with_cookie_token(self, mock_users_dao, mock_settings, mock_async_session):
        from unittest.mock import AsyncMock, MagicMock

        from fastapi import Request

        mock_user = MagicMock()
        mock_user.id = "user_id_123"
        mock_users_dao.find_by_id = AsyncMock(return_value=mock_user)

        mock_security = MagicMock()
        mock_payload = MagicMock()
        mock_payload.sub = "user_id_123"
        mock_payload.exp = datetime.now(UTC) + timedelta(hours=1)
        mock_security.verify_token.return_value = mock_payload
        mock_security.config.JWT_ACCESS_COOKIE_NAME = "_at"
        mock_security.config.JWT_ACCESS_CSRF_COOKIE_NAME = "_csrf"
        mock_settings.security = mock_security

        mock_session = AsyncMock()
        mock_async_session.return_value.__aenter__.return_value = mock_session
        mock_async_session.return_value.__aexit__ = AsyncMock()

        request = MagicMock(spec=Request)
        request.cookies.get.return_value = "cookie_token"
        request.headers.get.return_value = None

        user = await required_user(request)

        assert user == mock_user
        mock_security.verify_token.assert_called_once()
        mock_users_dao.find_by_id.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.session.settings")
    async def test_required_user_no_token(self, mock_settings):
        from unittest.mock import MagicMock

        from fastapi import Request

        mock_security = MagicMock()
        mock_security.config.JWT_ACCESS_COOKIE_NAME = "_at"
        mock_settings.security = mock_security

        request = MagicMock(spec=Request)
        request.cookies.get.return_value = None
        request.headers.get.return_value = None

        with pytest.raises(Unauthorized):
            await required_user(request)

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.session.async_session")
    @patch("app.utils.session.settings")
    @patch("app.utils.session.UsersDAO")
    async def test_required_user_expired_token(self, mock_users_dao, mock_settings, mock_async_session):
        from unittest.mock import MagicMock

        from fastapi import Request

        mock_security = MagicMock()
        mock_payload = MagicMock()
        mock_payload.exp = datetime.now(UTC) - timedelta(hours=1)
        mock_security.verify_token.return_value = mock_payload
        mock_security.config.JWT_ACCESS_COOKIE_NAME = "_at"
        mock_settings.security = mock_security

        request = MagicMock(spec=Request)
        request.cookies.get.return_value = "cookie_token"
        request.headers.get.return_value = None

        with pytest.raises(Unauthorized):
            await required_user(request)

    @pytest.mark.unit
    @pytest.mark.asyncio
    @patch("app.utils.session.async_session")
    @patch("app.utils.session.settings")
    @patch("app.utils.session.UsersDAO")
    async def test_required_user_not_found(self, mock_users_dao, mock_settings, mock_async_session):
        from unittest.mock import AsyncMock, MagicMock

        from fastapi import Request

        mock_users_dao.find_by_id = AsyncMock(return_value=None)

        mock_security = MagicMock()
        mock_payload = MagicMock()
        mock_payload.sub = "user_id_123"
        mock_payload.exp = datetime.now(UTC) + timedelta(hours=1)
        mock_security.verify_token.return_value = mock_payload
        mock_security.config.JWT_ACCESS_COOKIE_NAME = "_at"
        mock_settings.security = mock_security

        mock_session = AsyncMock()
        mock_async_session.return_value.__aenter__.return_value = mock_session
        mock_async_session.return_value.__aexit__ = AsyncMock()

        request = MagicMock(spec=Request)
        request.cookies.get.return_value = "cookie_token"
        request.headers.get.return_value = None

        with pytest.raises(UserDoesntExists):
            await required_user(request)

