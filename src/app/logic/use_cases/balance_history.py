from app.logic.abstract.balance_history_storage import (
    BalanceHistoryAllSelector,
)
from app.logic.models import BalanceChange


class GetMyBalanceHistory:
    def __init__(self, balance_history: BalanceHistoryAllSelector) -> None:
        self._balance_history = balance_history

    async def __call__(self, user_id: int) -> list[BalanceChange]:
        return await self._balance_history.select_all_user_history(user_id)
