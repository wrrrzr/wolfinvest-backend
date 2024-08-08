import asyncio
from typing import Iterable

from app.logic.abstract.symbols_getter import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory, SymbolPrice, SymbolHistoryInterval


class MultiSymbolsGetter(SymbolsGetter):
    def __init__(self, *getters: SymbolsGetter) -> None:
        self._getters = getters

    async def get_price(self, symbol: str) -> SymbolPrice:
        for getter in self._getters:
            try:
                return await getter.get_price(symbol)
            except UnfoundSymbolError:
                continue
        raise UnfoundSymbolError(f"Cannot find symbol {symbol}")

    async def get_many_prices(
        self, symbols: Iterable[str]
    ) -> list[SymbolPrice]:
        price_tasks = [self.get_price(i) for i in symbols]
        return await asyncio.gather(*price_tasks)

    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        for getter in self._getters:
            try:
                return await getter.get_history(interval, symbol)
            except UnfoundSymbolError:
                continue
        raise UnfoundSymbolError(f"Cannot find symbol {symbol}")
