from dataclasses import dataclass

from app.logic.abstract import SymbolsStorage
from app.logic.models import Symbol


@dataclass
class SymbolsMemory:
    amount: dict[int, dict[str, int]]
    owner: dict[int, dict[str, Symbol]]


def create_symbols_memory() -> SymbolsMemory:
    return SymbolsMemory({}, {})


class SymbolsCacheStorage(SymbolsStorage):
    def __init__(self, inner: SymbolsStorage, memory: SymbolsMemory) -> None:
        self._inner = inner
        self._memory = memory

    async def insert_or_add(
        self, owner_id: int, code: str, amount: int
    ) -> None:
        if owner_id not in self._memory.amount:
            self._memory.amount[owner_id] = {}
        if code not in self._memory.amount[owner_id]:
            self._memory.amount[owner_id][code] = await self._inner.get_amount(
                owner_id, code
            )
        self._memory.amount[owner_id][code] += amount
        await self._inner.insert_or_add(owner_id, code, amount)
        await self._update_owner(owner_id)

    async def get_amount(self, owner_id: int, code: str) -> int:
        if owner_id not in self._memory.amount:
            self._memory.amount[owner_id] = {}
        if code not in self._memory.amount[owner_id]:
            self._memory.amount[owner_id][code] = await self._inner.get_amount(
                owner_id, code
            )
        return self._memory.amount[owner_id][code]

    async def get_all_user_symbols(self, user_id: int) -> list[Symbol]:
        await self._check_exists_or_update(user_id)
        return list(self._memory.owner[user_id].values())

    async def remove(self, owner_id: int, code: str, amount: int) -> None:
        await self._inner.remove(owner_id, code, amount)
        await self._update_owner(owner_id)
        self._memory.amount[owner_id][code] -= amount

    async def _check_exists_or_update(self, owner_id: int) -> None:
        if owner_id not in self._memory.owner:
            await self._update_owner(owner_id)

    async def _update_owner(self, owner_id: int) -> None:
        symbols = await self._inner.get_all_user_symbols(owner_id)
        self._memory.owner[owner_id] = {i.code: i for i in symbols}
