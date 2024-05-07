from datetime import datetime

from app.logic.abstract import RefillsStorage
from app.logic.models import Refill

_memory_users_refills: dict[int, list[Refill]] = {}


class RefillsCacheStorage(RefillsStorage):
    def __init__(self, inner: RefillsStorage) -> None:
        self._inner = inner

    async def insert(
        self, user_id: int, amount: int, created_at: datetime
    ) -> None:
        await self._inner.insert(user_id, amount, created_at)
        _memory_users_refills[user_id] = (
            await self._inner.get_all_user_refills(user_id)
        )

    async def get_all_user_refills(self, user_id: int) -> list[Refill]:
        if user_id not in _memory_users_refills:
            _memory_users_refills[user_id] = (
                await self._inner.get_all_user_refills(user_id)
            )
        return _memory_users_refills[user_id]
