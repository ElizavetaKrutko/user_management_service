import datetime
import enum
import uuid
from typing import List, Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserORM(Base):
    __tablename__ = "user_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    surname: Mapped[Optional[str]] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    role: Mapped[Role] = mapped_column(nullable=True)
    image_path: Mapped[str] = mapped_column(nullable=True)
    is_blocked: Mapped[bool] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group_table.id"))

    groups: Mapped["GroupORM"] = relationship(back_populates="users")


class GroupORM(Base):
    __tablename__ = "group_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    users: Mapped[List["UserORM"]] = relationship(
        back_populates="groups", lazy="selectin"
    )
