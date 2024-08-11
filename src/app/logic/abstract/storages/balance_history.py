from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models import BalanceChangeReason, BalanceChange


class BalanceHistoryEditor(ABC):
    @abstractmethod
    async def add_balance(
        self,
        reason: BalanceChangeReason,
        created_at: datetime,
        user_id: int,
        balance: float,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_balance(
        self,
        reason: BalanceChangeReason,
        created_at: datetime,
        user_id: int,
        balance: float,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_balance(
        self,
        reason: BalanceChangeReason,
        created_at: datetime,
        user_id: int,
        balance: float,
    ) -> None:
        raise NotImplementedError


class BalanceHistoryAllSelector(ABC):
    @abstractmethod
    async def select_all_user_history(
        self, user_id: int
    ) -> list[BalanceChange]:
        raise NotImplementedError
