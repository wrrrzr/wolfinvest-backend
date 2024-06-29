from typing import Optional
from datetime import timedelta, datetime
from dataclasses import dataclass

from app.logic.abstract import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory, SymbolPrice
from app.utils.funcs import get_current_time

TIME_EXP_PRICE = timedelta(minutes=10)
TIME_EXP_DAILY_HISTORY = timedelta(minutes=30)


@dataclass
class CachedSymbolPrice:
    price: Optional[SymbolPrice]
    time_exp_cache: datetime


@dataclass
class CachedSymbolDailyHistory:
    history: Optional[list[SymbolHistory]]
    time_exp_cache: datetime


@dataclass
class MemorySymbolsGetter:
    price: dict[str, CachedSymbolPrice]
    daily_history: dict[str, CachedSymbolDailyHistory]


def create_symbols_getter_memory() -> MemorySymbolsGetter:
    return MemorySymbolsGetter({}, {})


class SymbolsGetterCache(SymbolsGetter):
    def __init__(
        self,
        inner: SymbolsGetter,
        memory: MemorySymbolsGetter,
    ) -> None:
        self._inner = inner
        self._memory = memory

    async def get_price(self, symbol: str) -> SymbolPrice:
        if symbol not in self._memory.price:
            await self._set_price(symbol)
        if self._memory.price[symbol].price is None:
            raise UnfoundSymbolError()
        if self._memory.price[symbol].time_exp_cache < get_current_time():
            await self._set_price(symbol)
        return self._memory.price[symbol].price

    async def get_daily_history(self, symbol: str) -> list[SymbolHistory]:
        if symbol not in self._memory.daily_history:
            await self._set_daily_history(symbol)
        if self._memory.daily_history[symbol].history is None:
            raise UnfoundSymbolError()
        if (
            self._memory.daily_history[symbol].time_exp_cache
            < get_current_time()
        ):
            await self._set_daily_history(symbol)
        return self._memory.daily_history[symbol].history

    async def _set_price(self, symbol: str) -> None:
        try:
            price = await self._inner.get_price(symbol)
        except UnfoundSymbolError:
            price = None
        self._memory.price[symbol] = CachedSymbolPrice(
            price, get_current_time() + TIME_EXP_PRICE
        )

    async def _set_daily_history(self, symbol: str) -> None:
        try:
            history = await self._inner.get_daily_history(symbol)
        except UnfoundSymbolError:
            history = None
        self._memory.daily_history[symbol] = CachedSymbolDailyHistory(
            history, get_current_time() + TIME_EXP_DAILY_HISTORY
        )
