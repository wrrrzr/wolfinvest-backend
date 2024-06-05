from typing import Optional
from datetime import timedelta
from dataclasses import dataclass

from app.logic.abstract import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.utils.funcs import get_current_time

TIME_EXP_PRICE = timedelta(minutes=10)
TIME_EXP_DAILY_HISTORY = timedelta(minutes=30)


@dataclass
class CachedSymbolPrice:
    price: Optional[float]
    time_exp_cache: timedelta


@dataclass
class CachedSymbolDailyHistory:
    history: Optional[list[float]]
    time_exp_cache: timedelta


_memory: dict[str, CachedSymbolPrice] = {}
_memory_daily_history: dict[str, CachedSymbolDailyHistory] = {}


class SymbolsGetterCache(SymbolsGetter):
    def __init__(self, inner: SymbolsGetter) -> None:
        self._inner = inner

    async def get_price(self, symbol: str) -> float:
        if symbol not in _memory:
            await self._set_price(symbol)
        if _memory[symbol].price is None:
            raise UnfoundSymbolError()
        if _memory[symbol].time_exp_cache < get_current_time():
            await self._set_price(symbol)
        return _memory[symbol].price

    async def get_daily_history(self, symbol: str) -> list[float]:
        if symbol not in _memory_daily_history:
            await self._set_daily_history(symbol)
        if _memory_daily_history[symbol].history is None:
            raise UnfoundSymbolError()
        if _memory_daily_history[symbol].time_exp_cache < get_current_time():
            await self._set_daily_history(symbol)
        return _memory_daily_history[symbol].history

    async def _set_price(self, symbol: str) -> None:
        try:
            price = await self._inner.get_price(symbol)
        except UnfoundSymbolError:
            price = None
        _memory[symbol] = CachedSymbolPrice(
            price, get_current_time() + TIME_EXP_PRICE
        )

    async def _set_daily_history(self, symbol: str) -> None:
        try:
            history = await self._inner.get_daily_history(symbol)
        except UnfoundSymbolError:
            history = None
        _memory_daily_history[symbol] = CachedSymbolDailyHistory(
            history, get_current_time() + TIME_EXP_DAILY_HISTORY
        )
