from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.db.models import Role


class TokensResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: int
    jwt_uuid: str


class UserBaseRead(BaseModel):
    id: UUID
    role: Role
    group_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: str
    password: str
    phone_number: str
    email: str
    role: Optional[Role] = Role.USER
    image_path: Optional[str]
    is_blocked: Optional[bool] = False
    group_id: int


class UserLogin(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    role: Optional[str]
    image_path: Optional[str]
    is_blocked: Optional[str]
