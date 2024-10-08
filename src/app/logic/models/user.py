from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, auto


class Role(IntEnum):
    USER = auto()
    OWNER = auto()


USER_DEFAULT_ROLE = Role.USER


@dataclass
class User:
    id: int
    username: str
    password: str
    role: int
    register_at: datetime
