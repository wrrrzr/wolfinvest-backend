from abc import ABC, abstractmethod
from typing import Iterable

from app.logic.models import SymbolTicker


class TickerFinder(ABC):
    @abstractmethod
    async def find_ticker(self, name: str) -> list[SymbolTicker]:
        raise NotImplementedError

    @abstractmethod
    async def get_name_by_ticker(self, ticker: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_names_by_tickers(self, tickers: Iterable[str]) -> list[str]:
        raise NotImplementedError
