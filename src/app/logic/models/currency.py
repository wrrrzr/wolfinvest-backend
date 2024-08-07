from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, auto


class Action(IntEnum):
    buy = auto()
    sell = auto()


@dataclass
class Currency:
    id: int
    user_id: int
    ticker: str
    amount: float


@dataclass
class CurrencyAction:
    user_id: int
    ticker: str
    action: int
    amount: int
    price: float
    created_at: datetime


@dataclass
class MyCurrencyDTO:
    ticker: str
    amount: float


@dataclass
class UserCurrencyData:
    amount: float
    actions: list[CurrencyAction]
