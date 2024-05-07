from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models import Refill


class RefillsStorage(ABC):
    @abstractmethod
    async def insert(
        self, user_id: int, amount: int, created_at: datetime
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_user_refills(self, user_id: int) -> list[Refill]:
        raise NotImplementedError
