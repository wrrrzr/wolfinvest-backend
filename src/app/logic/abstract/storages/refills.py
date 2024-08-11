from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models import Refill


class RefillsAdder(ABC):
    @abstractmethod
    async def insert(
        self, user_id: int, amount: int, created_at: datetime
    ) -> None:
        raise NotImplementedError


class RefillsUsersSelector(ABC):
    @abstractmethod
    async def get_all_user_refills(self, user_id: int) -> list[Refill]:
        raise NotImplementedError


class RefillsUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_refills(self, user_id: int) -> None:
        raise NotImplementedError


class RefillsStorage(
    RefillsAdder, RefillsUsersSelector, RefillsUsersDeletor, ABC
):
    pass
