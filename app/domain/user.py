from dataclasses import asdict, dataclass
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
    password: Optional[str] = None
    role: Role = None
    name: Optional[str] = None
    surname: Optional[str] = None
    username: str = None
    phone_number: str = None
    email: str = None
    image_path: Optional[str] = None
    group_id: Group = None
    is_blocked: bool = None
    id: UUID = None
    login: Optional[str] = None
    hashed_password: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items() if v is not None}
