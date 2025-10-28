from uuid import UUID

from pydantic import BaseModel

from app.utils.as_form import as_form


@as_form
class CreateUsersSchema(BaseModel):
    nickname: str
    email: str
    password: str

@as_form
class LoginUsersSchema(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    nickname: str

class UpdateUsersSchema(BaseModel):
    nickname: str
    email: str
