from dataclasses import dataclass
from datetime import datetime

from app.logic.abstract.storages.symbols import SymbolsStorage
from app.logic.models.symbol import SymbolAction, UserSymbolData


@dataclass
class SymbolsMemory:
    amount: dict[int, dict[str, int]]
    owner: dict[int, dict[str, UserSymbolData]]


class MemoryCacheSymbolsStorage(SymbolsStorage):
    def __init__(self, inner: SymbolsStorage, memory: SymbolsMemory) -> None:
        self._inner = inner
        self._memory = memory

    @staticmethod
    def create_memory() -> SymbolsMemory:
        return SymbolsMemory({}, {})

    async def add(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        created_at: datetime,
    ) -> None:
        if user_id not in self._memory.amount:
            self._memory.amount[user_id] = {}
        if ticker not in self._memory.amount[user_id]:
            self._memory.amount[user_id][ticker] = (
                await self._inner.get_amount(user_id, ticker)
            )
        await self._inner.add(user_id, ticker, amount, price, created_at)
        await self._update_owner(user_id)

    async def get_amount(self, user_id: int, ticker: str) -> int:
        if user_id not in self._memory.amount:
            self._memory.amount[user_id] = {}
        if ticker not in self._memory.amount[user_id]:
            self._memory.amount[user_id][ticker] = (
                await self._inner.get_amount(user_id, ticker)
            )
        return self._memory.amount[user_id][ticker]

    async def get_all_user_symbols(
        self, user_id: int
    ) -> dict[str, UserSymbolData]:
        return await self._inner.get_all_user_symbols(user_id)

    async def get_user_symbols_actions_by_symbol(
        self, user_id: int, ticker: str
    ) -> list[SymbolAction]:
        return await self._inner.get_user_symbols_actions_by_symbol(
            user_id, ticker
        )

    async def remove(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        created_at: datetime,
    ) -> None:
        await self._inner.remove(user_id, ticker, amount, price, created_at)
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
