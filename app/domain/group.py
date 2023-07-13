from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Group:
    id: int
    name: str
    created_at: Optional[datetime]
