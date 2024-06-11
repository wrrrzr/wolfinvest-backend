from dataclasses import dataclass
from enum import IntEnum, auto


class Role(IntEnum):
    USER = auto()
    OWNER = auto()


USER_DEFAULT_ROLE = Role.USER


@dataclass
class User:
    id: int
    balance: float
    username: str
    password: str
    role: int
