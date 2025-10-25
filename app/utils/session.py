from datetime import UTC, datetime, timedelta

import bcrypt
from authx.schema import RequestToken
from fastapi import Request, Response

from app.dao.users import UsersDAO
from app.db.config import async_session
from app.exceptions.api import Unauthorized, UserDoesntExists
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

async def required_user(request: Request):
    token = None
    if request.cookies.get(settings.security.config.JWT_ACCESS_COOKIE_NAME):
        token = RequestToken(
            token=request.cookies.get(settings.security.config.JWT_ACCESS_COOKIE_NAME),
            csrf=request.cookies.get(settings.security.config.JWT_ACCESS_CSRF_COOKIE_NAME),
            location="cookies"
        )
    elif request.headers.get("Authorization"):
        token = RequestToken(token=request.headers.get("Authorization").split()[-1], location="headers")
    if not token:
        raise Unauthorized

    if token.location == "cookies":
        payload = settings.security.verify_token(token, verify_csrf=True)
    else:
        payload = settings.security.verify_token(token, verify_csrf=False)

    if payload.exp < datetime.now(UTC):
        raise Unauthorized
    async with async_session() as session:
        user = await UsersDAO.find_by_id(session=session, model_id=payload.sub)
    if not user:
        raise UserDoesntExists

    return user
