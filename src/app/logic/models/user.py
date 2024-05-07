from dataclasses import dataclass


@dataclass
class User:
    id: int
    balance: float
    username: str
    password: str
