from datetime import UTC, datetime, timedelta

import bcrypt
from fastapi import Response

from app.settings import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def add_users_response_cookie(response: Response, user_id: str):
     settings.security.set_access_cookies(
        token = settings.security.create_access_token(
            uid=user_id,
            expiry=datetime.now(UTC) + timedelta(seconds=settings.JWT_EXPIRY_USER_SECONDS)
        ),
        response = response
    )
