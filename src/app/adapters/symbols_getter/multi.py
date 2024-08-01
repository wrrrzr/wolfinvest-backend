from app.logic.abstract import SymbolsGetter
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

    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        for getter in self._getters:
            try:
                return await getter.get_history(interval, symbol)
            except UnfoundSymbolError:
                continue
        raise UnfoundSymbolError(f"Cannot find symbol {symbol}")
