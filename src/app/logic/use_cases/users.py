from dataclasses import dataclass
from datetime import datetime

from app.logic.abstract import UsersOneSelector
from app.logic.abstract.currency_storage import (
    CurrencyAmountSelector,
    MAIN_CURRENCY,
)


@dataclass
class UserGetMeDTO:
    id: int
    balance: float
    username: str
    role: int
    register_at: datetime


class GetMe:
    def __init__(
        self, users: UsersOneSelector, currency_amount: CurrencyAmountSelector
    ) -> None:
        self._users = users
        self._currency_amount = currency_amount

    async def __call__(self, user_id: int) -> UserGetMeDTO:
        res = await self._users.select_one_by_id(user_id)
        balance = await self._currency_amount.get_amount(
            user_id, MAIN_CURRENCY
        )
        return UserGetMeDTO(
            id=res.id,
            balance=balance,
            username=res.username,
            role=res.role,
            register_at=res.register_at,
        )
