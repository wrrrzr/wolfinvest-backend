import asyncio
from typing import Optional, Iterable
from datetime import timedelta, datetime
from dataclasses import dataclass
from collections import defaultdict

from app.logic.abstract.symbols_getter import SymbolsGetter
from app.logic.abstract.clock import ClockCurrentTimeGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory, SymbolPrice, SymbolHistoryInterval

TIME_EXP_PRICE = timedelta(minutes=10)
TIME_EXP_HISTORY = timedelta(minutes=30)


@dataclass
class CachedSymbolPrice:
    price: Optional[SymbolPrice]
    time_exp_cache: datetime


@dataclass
class CachedSymbolHistory:
    history: Optional[dict[SymbolHistoryInterval, list[SymbolHistory]]]
    time_exp_cache: datetime


@dataclass
class MemorySymbolsGetter:
    price: dict[str, CachedSymbolPrice]
    history: dict[str, CachedSymbolHistory]
    price_locks: dict[str, asyncio.Lock]
    history_locks: dict[SymbolHistoryInterval, dict[str, asyncio.Lock]]


class MemoryCacheSymbolsGetter(SymbolsGetter):
    def __init__(
        self,
        inner: SymbolsGetter,
        memory: MemorySymbolsGetter,
        clock: ClockCurrentTimeGetter,
    ) -> None:
        self._inner = inner
        self._memory = memory
        self._clock = clock

    @staticmethod
    def create_memory() -> MemorySymbolsGetter:
        return MemorySymbolsGetter(
            {},
            {},
            defaultdict(asyncio.Lock),
            defaultdict(lambda: defaultdict(asyncio.Lock)),
        )

    async def get_price(self, symbol: str) -> SymbolPrice:
        async with self._memory.price_locks[symbol]:
            if symbol not in self._memory.price:
                await self._set_price(symbol)
            if self._memory.price[symbol].price is None:
                raise UnfoundSymbolError(f"Cannot find symbol {symbol}")
            if (
                self._memory.price[symbol].time_exp_cache
                < await self._clock.get_current_time()
            ):
                await self._set_price(symbol)
            return self._memory.price[symbol].price

    async def get_many_prices(
        self, symbols: Iterable[str]
    ) -> list[SymbolPrice]:
        price_tasks = [self.get_price(i) for i in symbols]
        return await asyncio.gather(*price_tasks)

    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        async with self._memory.history_locks[interval][symbol]:
            if (
                symbol not in self._memory.history
                or interval not in self._memory.history[symbol].history
            ):
                await self._set_history(interval, symbol)
            if self._memory.history[symbol].history is None:
                raise UnfoundSymbolError(f"Cannot find symbol {symbol}")
            if (
                self._memory.history[symbol].time_exp_cache
                < await self._clock.get_current_time()
            ):
                await self._set_history(interval, symbol)
            return self._memory.history[symbol].history[interval]

    async def _set_price(self, symbol: str) -> None:
        try:
            price = await self._inner.get_price(symbol)
        except UnfoundSymbolError:
            price = None
        self._memory.price[symbol] = CachedSymbolPrice(
            price, await self._clock.get_current_time() + TIME_EXP_PRICE
        )

    async def _set_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> None:
        try:
            history = await self._inner.get_history(interval, symbol)
        except UnfoundSymbolError:
            history = None
        if history is None:
            self._memory.history[symbol] = CachedSymbolHistory(
                None, await self._clock.get_current_time()
            )
            return
        if symbol not in self._memory.history:
            self._memory.history[symbol] = CachedSymbolHistory(
                {}, await self._clock.get_current_time() + TIME_EXP_HISTORY
            )
        self._memory.history[symbol].history[interval] = history
