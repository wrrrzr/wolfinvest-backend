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
class SymbolInList:
    code: str
    name: str
    price: SymbolPrice


@dataclass
class SymbolHistory:
    price: SymbolPrice
    timestamp: datetime
