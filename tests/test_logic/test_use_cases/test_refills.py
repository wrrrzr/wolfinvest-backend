from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.logic.abstract.storages.currency import MAIN_CURRENCY
from app.logic.models.currency import Reason
from app.logic.models.refill import Refill
from app.logic.use_cases.refills import TakeRefill, GetMyRefills, MyRefillDTO
from app.logic.dataclasses import objects_to_dataclasses


async def test_take_refill() -> None:
    USER_ID = 42
    AMOUNT = 100
    users_balance = AsyncMock()
    refills_adder = AsyncMock()
    transaction = AsyncMock()
    clock = AsyncMock()
    mocktime = datetime.now(timezone.utc)
    clock.get_current_time.return_value = mocktime
    use_case = TakeRefill(users_balance, refills_adder, transaction, clock)

    await use_case(USER_ID, AMOUNT)
    refills_adder.insert.assert_awaited_once_with(USER_ID, AMOUNT, mocktime)
    users_balance.add.assert_awaited_once_with(
        USER_ID, MAIN_CURRENCY, AMOUNT, 1.0, Reason.taken_refill
    )
    transaction.commit.assert_awaited_once()


async def test_get_my_refills() -> None:
    USER_ID = 1515
    RETURN_VALUE = [
        Refill(1, USER_ID, 100, datetime.now(timezone.utc)),
        Refill(2, USER_ID, 500, datetime.now(timezone.utc)),
    ]
    refills_selector = AsyncMock()
    refills_selector.get_all_user_refills.return_value = RETURN_VALUE
    use_case = GetMyRefills(refills_selector)

    assert await use_case(USER_ID) == objects_to_dataclasses(
        RETURN_VALUE, MyRefillDTO
    )
    refills_selector.get_all_user_refills.assert_awaited_once_with(USER_ID)
