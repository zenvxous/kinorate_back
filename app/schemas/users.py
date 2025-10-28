from uuid import UUID

from pydantic import BaseModel

from app.utils.as_form import as_form


@as_form
class CreateUserSchema(BaseModel):
    nickname: str
    email: str
    password: str

@as_form
class LoginUserSchema(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    nickname: str

class UpdateUserSchema(BaseModel):
    nickname: str
    email: str
