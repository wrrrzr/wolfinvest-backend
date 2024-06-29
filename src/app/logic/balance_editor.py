from app.logic.abstract import UsersStorage, BalanceHistoryEditor
from app.logic.models import BalanceChangeReason
from app.utils.funcs import get_current_time


class BalanceEditor:
    def __init__(
        self, users: UsersStorage, balance_history: BalanceHistoryEditor
    ) -> None:
        self._users = users
        self._balance_history = balance_history

    async def add_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        await self._users.add_balance(user_id, balance)
        await self._balance_history.add_balance(
            reason, get_current_time(), user_id, balance
        )

    async def remove_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        await self._users.remove_balance(user_id, balance)
        await self._balance_history.remove_balance(
            reason, get_current_time(), user_id, balance
        )

    async def set_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        await self._users.set_balance(user_id, balance)
        await self._balance_history.set_balance(
            reason, get_current_time(), user_id, balance
        )
