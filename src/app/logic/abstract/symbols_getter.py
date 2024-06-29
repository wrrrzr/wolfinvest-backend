from abc import ABC, abstractmethod

from app.logic.models import SymbolHistory, SymbolPrice, SymbolHistoryInterval


class SymbolsPriceGetter(ABC):
    @abstractmethod
    async def get_price(self, symbol: str) -> SymbolPrice:
        raise NotImplementedError


class SymbolsHistoryGetter(ABC):
    @abstractmethod
    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        raise NotImplementedError


class SymbolsGetter(SymbolsPriceGetter, SymbolsHistoryGetter, ABC):
    pass
