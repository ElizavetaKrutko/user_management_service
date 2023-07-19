from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.adapters.orm_engines.models import Role
from app.domain.user import User


class TokensResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
    exp: int
    jwt_uuid: UUID


class UserBaseRead(BaseModel):
    id: UUID
    role: Role
    group_id: int

    class Config:
        orm_mode = True


class UserInfo(UserBaseRead):
    name: Optional[str]
    surname: Optional[str]
    username: str
    phone_number: str
    email: str
    image_path: Optional[str]
    is_blocked: Optional[bool] = False


class UserPublicInfo(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: str
    phone_number: str
    email: str
    role: Optional[Role] = Role.USER
    image_path: Optional[str]

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

    def to_entity(self):
        return User(
            name=self.name,
            surname=self.surname,
            username=self.username,
            password=self.password,
            phone_number=self.phone_number,
            email=self.email,
            role=self.role,
            image_path=self.image_path,
            is_blocked=self.is_blocked,
            group_id=self.group_id,
        )


class UserLogin(BaseModel):
    login: str
    password: str

    def to_entity(self):
        return User(
            login=self.login,
            password=self.password,
        )

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    role: Optional[Role]
    image_path: Optional[str]
    is_blocked: Optional[bool]

    def to_entity(self):
        return User(
            name=self.name,
            surname=self.surname,
            username=self.username,
            phone_number=self.phone_number,
            email=self.email,
            role=self.role,
            image_path=self.image_path,
            is_blocked=self.is_blocked,
        )
