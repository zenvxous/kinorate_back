from typing import Annotated

from fastapi import APIRouter, Form, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.users import UserDAO
from app.db.config import get_db
from app.exceptions.api import (
    InvalidCredentials,
    InvalidEmail,
    UserAlreadyExists,
)
from app.schemas.users import CreateUsersSchema, LoginUsersSchema
from app.settings import settings
from app.utils.common import is_valid_email
from app.utils.session import (
    add_users_response_cookie,
    hash_password,
    verify_password,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register")
async def register_user(
    data: Annotated[CreateUsersSchema, Form()],
    session: AsyncSession = Depends(get_db),
):
    if not is_valid_email(data.email):
        raise InvalidEmail

    users = await UserDAO.get_by_email_or_nickname(session=session, email=data.email, nickname=data.nickname)
    if users:
        raise UserAlreadyExists

    await UserDAO.add(
        session,
        email=data.email,
        nickname=data.nickname,
        password_hash=hash_password(data.password),
    )
    await session.commit()

@router.post("/login")
async def login_user(
    data: Annotated[LoginUsersSchema, Form()],
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    user = await UserDAO.get_by_email(session=session, email=data.email)
    if not user:
        raise InvalidCredentials

    if verify_password(data.password, user.password_hash):
        add_users_response_cookie(response, str(user.id))
    else :
        raise InvalidCredentials

@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie(
        key=settings.security.config.JWT_ACCESS_COOKIE_NAME,
        path=settings.security.config.JWT_ACCESS_COOKIE_PATH,
        domain=settings.security.config.JWT_COOKIE_DOMAIN,
        secure=settings.security.config.JWT_COOKIE_SECURE,
        samesite=settings.security.config.JWT_COOKIE_SAMESITE,
    )
    if settings.security.config.JWT_COOKIE_CSRF_PROTECT and settings.security.config.JWT_CSRF_IN_COOKIES:
        response.delete_cookie(
            key=settings.security.config.JWT_ACCESS_CSRF_COOKIE_NAME,
            path=settings.security.config.JWT_ACCESS_CSRF_COOKIE_PATH,
            domain=settings.security.config.JWT_COOKIE_DOMAIN,
            secure=settings.security.config.JWT_COOKIE_SECURE,
            samesite=settings.security.config.JWT_COOKIE_SAMESITE,
        )
