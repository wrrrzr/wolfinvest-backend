from dataclasses import dataclass
from datetime import datetime


@dataclass
class Refill:
    id: int
    user_id: int
    amount: int
    created_at: datetime
