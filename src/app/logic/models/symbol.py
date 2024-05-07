from dataclasses import dataclass


@dataclass
class Symbol:
    id: int
    owner_id: int
    code: str
    amount: int
