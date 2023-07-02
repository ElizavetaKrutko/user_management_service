import datetime
import uuid
from typing import List, Literal, Optional

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


Role = Literal["USER", "ADMIN", "MODERATOR"]


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[Optional[str]]
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(15))
    phone_number: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(30))
    role: Mapped[Role]
    image_path: Mapped[str]
    is_blocked: Mapped[bool]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime.datetime]
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))

    groups: Mapped["Group"] = relationship(back_populates="users")


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    users: Mapped[List["User"]] = relationship(back_populates="groups", lazy="selectin")
