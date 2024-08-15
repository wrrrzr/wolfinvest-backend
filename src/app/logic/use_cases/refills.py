from dataclasses import dataclass
from datetime import datetime

from app.utils.dataclasses import objects_to_dataclasses
from app.logic.models.currency import Reason
from app.logic.abstract.storages.refills import (
    RefillsAdder,
    RefillsUsersSelector,
)
from app.logic.abstract.transaction import Transaction
from app.logic.abstract.clock import ClockCurrentTimeGetter
from app.logic.abstract.storages.currency import CurrencyAdder, MAIN_CURRENCY


class TakeRefill:
    def __init__(
        self,
        users_balance: CurrencyAdder,
        refills: RefillsAdder,
        transaction: Transaction,
        clock: ClockCurrentTimeGetter,
    ) -> None:
        self._users_balance = users_balance
        self._refills = refills
        self._transaction = transaction
        self._clock = clock

    async def __call__(self, user_id: int, amount: int) -> None:
        await self._refills.insert(
            user_id, amount, await self._clock.get_current_time()
        )
        await self._users_balance.add(
            user_id, MAIN_CURRENCY, amount, 1.0, Reason.taken_refill
        )
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
