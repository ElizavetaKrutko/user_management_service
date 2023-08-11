from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Group:
    id: int
    name: str
    created_at: Optional[datetime]
    created_at: Optional[datetime] = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items() if v is not None}
