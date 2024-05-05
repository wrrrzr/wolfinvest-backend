from dataclasses import dataclass


@dataclass
class User:
    id: int
    balance: int
    username: str
    password: str
