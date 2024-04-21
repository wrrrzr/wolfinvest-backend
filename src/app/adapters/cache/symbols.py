from typing import Optional
from datetime import timedelta
from dataclasses import dataclass

from app.logic.abstract import SymbolsStorage
from app.utils.funcs import get_current_time

TIME_EXP = timedelta(minutes=5)


@dataclass
class CachedSymbol:
    price: Optional[float]
    time_exp_cache: timedelta


_memory: dict[str, CachedSymbol] = {}


class SymbolsCacheStorage(SymbolsStorage):
    def __init__(self, inner: SymbolsStorage) -> None:
        self._inner = inner

    async def get_price_or_none(self, symbol: str) -> Optional[float]:
        if (
            symbol not in _memory
            or _memory[symbol].time_exp_cache > get_current_time()
        ):
            price = await self._inner.get_price_or_none(symbol)
            _memory[symbol] = CachedSymbol(
                price, get_current_time() + TIME_EXP
            )
        return _memory[symbol].price
