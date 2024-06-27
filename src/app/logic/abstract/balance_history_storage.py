from abc import ABC, abstractmethod

from app.logic.models import BalanceChangeReason, BalanceChange


class BalanceHistoryStorage(ABC):
    @abstractmethod
    async def add_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_all_user_history(
        self, user_id: int
    ) -> list[BalanceChange]:
        raise NotImplementedError
