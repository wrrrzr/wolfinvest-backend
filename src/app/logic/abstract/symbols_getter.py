from abc import ABC, abstractmethod

from app.logic.models import SymbolHistory, SymbolPrice


class SymbolsGetter(ABC):
    @abstractmethod
    async def get_price(self, symbol: str) -> SymbolPrice:
        raise NotImplementedError

    @abstractmethod
    async def get_daily_history(self, symbol: str) -> list[SymbolHistory]:
        raise NotImplementedError
