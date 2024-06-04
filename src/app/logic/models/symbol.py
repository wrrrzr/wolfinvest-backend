from dataclasses import dataclass

DEFAULT_AMOUNT = 0


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
    price: float
