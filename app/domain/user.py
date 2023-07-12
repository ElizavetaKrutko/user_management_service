from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from app.domain.group import Group


class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


@dataclass
class User:
    id: UUID
    name: Optional[str]
    surname: Optional[str]
    username: str
    hashed_password: str
    phone_number: str
    email: str
    image_path: Optional[str]
    created_at: datetime
    modified_at: datetime
    role: Role = Role.USER
    is_blocked: bool = False
    group: Group = None
