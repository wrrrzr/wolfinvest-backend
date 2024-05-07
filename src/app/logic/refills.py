from dataclasses import dataclass
from datetime import datetime

from app.utils.funcs import get_current_time
from app.utils.dataclasses import object_to_dataclass
from .abstract import UsersStorage, RefillsStorage


class TakeRefill:
    def __init__(self, users: UsersStorage, refills: RefillsStorage) -> None:
        self._users = users
        self._refills = refills

    async def __call__(self, user_id: int, amount: int) -> None:
        await self._refills.insert(user_id, amount, get_current_time())
        await self._users.add_balance(user_id, amount)


@dataclass
class MyRefillDTO:
    amount: int
    created_at: datetime


class GetMyRefills:
    def __init__(self, refills: RefillsStorage) -> None:
        self._refills = refills

    async def __call__(self, user_id: int) -> list[MyRefillDTO]:
        refills = await self._refills.get_all_user_refills(user_id)
        return [object_to_dataclass(i, MyRefillDTO) for i in refills]
