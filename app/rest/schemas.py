from typing import Optional

from pydantic import BaseModel


class TokensResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: int


class UserRead(BaseModel):
    id: int
    username: str
    role: str
    group_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: str
    password: str
    phone_number: Optional[str]
    email: Optional[str]
    role: Optional[str] = "user"
    image_path: Optional[str]
    is_blocked: Optional[str] = "False"
    group_id: int


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
