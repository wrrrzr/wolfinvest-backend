from dataclasses import dataclass

from app.logic.abstract.symbols_storage import SymbolsStorage
from app.logic.models.symbol import SymbolAction


@dataclass
class SymbolsMemory:
    amount: dict[int, dict[str, int]]
    owner: dict[int, dict[str, int]]


def create_symbols_memory() -> SymbolsMemory:
    return SymbolsMemory({}, {})


class SymbolsCacheStorage(SymbolsStorage):
    def __init__(self, inner: SymbolsStorage, memory: SymbolsMemory) -> None:
        self._inner = inner
        self._memory = memory

    async def add(
        self, user_id: int, ticker: str, amount: int, price: float
    ) -> None:
        if user_id not in self._memory.amount:
            self._memory.amount[user_id] = {}
        if ticker not in self._memory.amount[user_id]:
            self._memory.amount[user_id][ticker] = (
                await self._inner.get_amount(user_id, ticker)
            )
        await self._inner.add(user_id, ticker, amount, price)
        await self._update_owner(user_id)

    async def get_amount(self, user_id: int, ticker: str) -> int:
        if user_id not in self._memory.amount:
            self._memory.amount[user_id] = {}
        if ticker not in self._memory.amount[user_id]:
            self._memory.amount[user_id][ticker] = (
                await self._inner.get_amount(user_id, ticker)
            )
        return self._memory.amount[user_id][ticker]

    async def get_all_user_symbols(self, user_id: int) -> dict[str, int]:
        await self._check_exists_or_update(user_id)
        return self._memory.owner[user_id]

    async def get_user_symbols_actions_by_symbol(
        self, user_id: int, ticker: str
    ) -> list[SymbolAction]:
        return await self._inner.get_user_symbols_actions_by_symbol(
            user_id, ticker
        )

    async def remove(
        self, user_id: int, ticker: str, amount: int, price: float
    ) -> None:
        await self._inner.remove(user_id, ticker, amount, price)
        await self._update_owner(user_id)

    async def delete_all_user_symbols(self, user_id: int) -> None:
        await self._inner.delete_all_user_symbols(user_id)

    async def _check_exists_or_update(self, user_id: int) -> None:
        if user_id not in self._memory.owner:
            await self._update_owner(user_id)

    async def _update_owner(self, user_id: int) -> None:
        self._memory.owner[user_id] = await self._inner.get_all_user_symbols(
            user_id
        )
