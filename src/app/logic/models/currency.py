from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, auto
from typing import Any


class Action(IntEnum):
    add = auto()
    remove = auto()


class Reason(IntEnum):
    unknown_add = auto()
    unknown_remove = auto()
    buy = auto()
    sell = auto()
    buy_symbol = auto()
    sell_symbol = auto()
    taken_refill = auto()


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
    reason: int
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


@dataclass
class CurrencyChange:
    ticker: str
    amount: float
    reason: int
    created_at: datetime
    additional_info: dict[str, Any]


@dataclass
class CurrencySymbolInfo:
    symbol_ticker: str
    symbol_amount: int
