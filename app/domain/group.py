from dataclasses import dataclass
from datetime import datetime


@dataclass
class Group:
    id: int
    name: str
    created_at: datetime
