from dataclasses import dataclass
from datetime import datetime

from app.logic.abstract import RefillsStorage
from app.logic.models import Refill


@dataclass
class MemoryRefills:
    users_refills: dict[int, list[Refill]]


def create_refills_memory() -> MemoryRefills:
    return MemoryRefills({})


class RefillsCacheStorage(RefillsStorage):
    def __init__(self, inner: RefillsStorage, memory: MemoryRefills) -> None:
        self._inner = inner
        self._memory = memory

    async def insert(
        self, user_id: int, amount: int, created_at: datetime
    ) -> None:
        await self._inner.insert(user_id, amount, created_at)
        self._memory.users_refills[user_id] = (
            await self._inner.get_all_user_refills(user_id)
        )

    async def get_all_user_refills(self, user_id: int) -> list[Refill]:
        if user_id not in self._memory.users_refills:
            self._memory.users_refills[user_id] = (
                await self._inner.get_all_user_refills(user_id)
            )
        return self._memory.users_refills[user_id]
