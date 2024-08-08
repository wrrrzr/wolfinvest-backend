from dataclasses import dataclass
from datetime import datetime

from app.utils.funcs import get_current_time
from app.utils.dataclasses import objects_to_dataclasses
from app.logic.abstract.refills_storage import (
    RefillsAdder,
    RefillsUsersSelector,
)
from app.logic.abstract.transaction import Transaction
from app.logic.abstract.currency_storage import CurrencyAdder, MAIN_CURRENCY


class TakeRefill:
    def __init__(
        self,
        users_balance: CurrencyAdder,
        refills: RefillsAdder,
        transaction: Transaction,
    ) -> None:
        self._users_balance = users_balance
        self._refills = refills
        self._transaction = transaction

    async def __call__(self, user_id: int, amount: int) -> None:
        await self._refills.insert(user_id, amount, get_current_time())
        await self._users_balance.add(user_id, MAIN_CURRENCY, amount, 1.0)
        await self._transaction.commit()


@dataclass
class MyRefillDTO:
    amount: int
    created_at: datetime


class GetMyRefills:
    def __init__(self, refills: RefillsUsersSelector) -> None:
        self._refills = refills

    async def __call__(self, user_id: int) -> list[MyRefillDTO]:
        refills = await self._refills.get_all_user_refills(user_id)
        return objects_to_dataclasses(refills, MyRefillDTO)
