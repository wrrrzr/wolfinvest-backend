from datetime import datetime

import pytest

from app.logic.abstract.storages.users import UsersOneSelector
from app.logic.abstract.storages.currency import (
    CurrencyAmountSelector,
    MAIN_CURRENCY,
)
from app.logic.models import User, USER_DEFAULT_ROLE
from app.logic.use_cases.users import GetMe, UserGetMeDTO


class MockAmountSelector(CurrencyAmountSelector):
    async def get_amount(self, user_id: int, ticker: str) -> float:
        if ticker == MAIN_CURRENCY:
            return 1.5
        return 2.2


class MockUsersStorage(UsersOneSelector):
    async def select_one_by_username() -> None:
        pass

    async def select_one_by_id(self, user_id: int) -> User:
        return User(
            id=user_id,
            username=f"user{user_id}",
            password=f"{user_id}password",
            role=USER_DEFAULT_ROLE,
            register_at=datetime.now(),
        )


@pytest.mark.parametrize("id", [5, 1, 5, 123456719])
async def test_get_me(id: int) -> None:
    use_case = GetMe(MockUsersStorage(), MockAmountSelector())
    res = await use_case(id)
    assert isinstance(res, UserGetMeDTO)
    assert res.id == id
    assert res.username == f"user{id}"
    assert res.balance == 1.5
