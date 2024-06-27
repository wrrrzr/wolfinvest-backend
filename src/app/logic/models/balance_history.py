from enum import IntEnum
from dataclasses import dataclass


class BalanceChangeReason(IntEnum):
    taked_refill = 0
    admin_set = 1
    buy_symbol = 2
    sold_symbol = 3


class BalanceChangeType(IntEnum):
    set = 0
    add = 1
    remove = 2


@dataclass
class BalanceChange:
    change_type: int
    amount: float
    reason: int
