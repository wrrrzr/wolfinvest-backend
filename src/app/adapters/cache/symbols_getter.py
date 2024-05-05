from typing import Optional
from datetime import timedelta
from dataclasses import dataclass

from app.logic.abstract import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.utils.funcs import get_current_time

TIME_EXP = timedelta(minutes=5)


@dataclass
class CachedSymbolPrice:
    price: Optional[float]
    time_exp_cache: timedelta


_memory: dict[str, CachedSymbolPrice] = {}


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

    async def _set_price(self, symbol: str) -> None:
        try:
            price = await self._inner.get_price(symbol)
        except UnfoundSymbolError:
            price = None
        _memory[symbol] = CachedSymbolPrice(
            price, get_current_time() + TIME_EXP
        )
