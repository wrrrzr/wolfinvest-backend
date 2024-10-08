from dataclasses import dataclass
from typing import Iterable

from app.logic.abstract.ticker_finder import TickerFinder
from app.logic.models import SymbolTicker


@dataclass
class TickerFinderMemory:
    data: dict[str, list[SymbolTicker]]
    data_names: dict[str, str]


class MemoryCacheTickerFinder(TickerFinder):
    def __init__(self, inner: TickerFinder, memory: TickerFinderMemory):
        self._inner = inner
        self._memory = memory

    @staticmethod
    def create_memory() -> TickerFinderMemory:
        return TickerFinderMemory({}, {})

    async def find_ticker(self, name: str) -> list[SymbolTicker]:
        if name not in self._memory.data:
            await self._add_to_cache(name)
        return self._memory.data[name]

    async def get_name_by_ticker(self, ticker: str) -> str:
        if ticker not in self._memory.data_names:
            await self._add_to_names_cache(ticker)
        return self._memory.data_names[ticker]

    async def get_names_by_tickers(self, tickers: Iterable[str]) -> list[str]:
        return await self._inner.get_names_by_tickers(tickers)

    async def _add_to_cache(self, name: str) -> None:
        self._memory.data[name] = await self._inner.find_ticker(name)
        return

    async def _add_to_names_cache(self, ticker: str) -> None:
        self._memory.data_names[ticker] = await self._inner.get_name_by_ticker(
            ticker
        )
        return
