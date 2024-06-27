from dataclasses import dataclass
from datetime import datetime

from app.utils.funcs import get_current_time
from app.utils.dataclasses import object_to_dataclass
from app.logic.abstract import RefillsStorage
from app.logic.models import BalanceChangeReason
from app.logic.balance_editor import BalanceEditor


class TakeRefill:
    def __init__(
        self, users_balance: BalanceEditor, refills: RefillsStorage
    ) -> None:
        self._users_balance = users_balance
        self._refills = refills

    async def __call__(self, user_id: int, amount: int) -> None:
        await self._refills.insert(user_id, amount, get_current_time())
        await self._users_balance.add_balance(
            BalanceChangeReason.taked_refill, user_id, amount
        )


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
