from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, auto

DEFAULT_AMOUNT = 0


class SymbolHistoryInterval(IntEnum):
    FIVE_MINUTES = auto()
    HOUR = auto()
    DAY = auto()
    WEEK = auto()
    MONTH = auto()
    THREE_MONTHS = auto()


class Action(IntEnum):
    buy = auto()
    sell = auto()


@dataclass
class SymbolPrice:
    buy: float
    sell: float


@dataclass
class SymbolData:
    price: SymbolPrice
    name: str


@dataclass
class Symbol:
    id: int
    owner_id: int
    code: str
    amount: int


@dataclass
class SymbolHistory:
    price: SymbolPrice
    timestamp: datetime


@dataclass
class SymbolTicker:
    name: str
    ticker: str


@dataclass
class SymbolAction:
    user_id: int
    ticker: str
    action: int
    amount: float
    created_at: datetime
