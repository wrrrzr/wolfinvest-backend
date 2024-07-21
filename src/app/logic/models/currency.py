from dataclasses import dataclass


@dataclass
class Currency:
    id: int
    user_id: int
    ticker: str
    amount: float
