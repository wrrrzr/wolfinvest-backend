from dataclasses import dataclass
from datetime import datetime

DEFAULT_AMOUNT = 0


@dataclass
class SymbolPrice:
    buy: float
    sell: float


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
