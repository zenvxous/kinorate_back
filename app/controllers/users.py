from typing import Annotated

from fastapi import APIRouter, Form, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.users import UsersDAO
from app.db.config import get_db
from app.exceptions.api import (
    InvalidCredentials,
    InvalidEmail,
    NoChangesError,
    UserAlreadyExists,
    UserEmailOrNicknameAlreadyExists,
)
from app.schemas.users import CreateUserSchema, LoginUserSchema, UpdateUserSchema, UserResponse
from app.settings import settings
from app.utils.common import is_valid_email
from app.utils.session import (
    add_users_response_cookie,
    hash_password,
    required_user,
    verify_password,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register", status_code= 201)
async def register_user(
    data: Annotated[CreateUserSchema, Form()],
    session: AsyncSession = Depends(get_db),
):
    if not is_valid_email(data.email):
        raise InvalidEmail

    users = await UsersDAO.get_by_email_or_nickname(session=session, email=data.email, nickname=data.nickname)
    if users:
        raise UserAlreadyExists

    await UsersDAO.add(
        session,
        email=data.email,
        nickname=data.nickname,
        password_hash=hash_password(data.password),
    )
    await session.commit()

@router.post("/login", status_code=204)
async def login_user(
    data: Annotated[LoginUserSchema, Form()],
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    user = await UsersDAO.get_by_email(session=session, email=data.email)
    if not user:
        raise InvalidCredentials

    if verify_password(data.password, user.password_hash):
        add_users_response_cookie(response, str(user.id))
    else :
        raise InvalidCredentials

@router.post("/logout", dependencies=[Depends(required_user)], status_code=204)
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

@router.get("/me", status_code=200)
async def get_me(user: UserResponse = Depends(required_user)) -> UserResponse:
    return user

@router.put("/me", status_code=200)
async def update_me(
    data: UpdateUserSchema,
    user = Depends(required_user),
    session: AsyncSession = Depends(get_db),
):
    if not is_valid_email(data.email):
        raise InvalidEmail

    if data.email == user.email and data.nickname == user.nickname:
        raise NoChangesError

    existing_users = await UsersDAO.get_by_email_or_nickname(session=session, email=data.email, nickname=data.nickname)

    for existing_user in existing_users:
        if existing_user.id != user.id:
            raise UserEmailOrNicknameAlreadyExists

    updated_user = await UsersDAO.update(
        session,
        id=user.id,
        nickname=data.nickname,
        email=data.email,
    )
    await session.commit()

    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        nickname=updated_user.nickname,
    )

@router.delete("/me", status_code=204)
async def delete_me(
    user = Depends(required_user),
    session: AsyncSession = Depends(get_db),
):
    await UsersDAO.delete(session=session, id=user.id)
    await session.commit()
