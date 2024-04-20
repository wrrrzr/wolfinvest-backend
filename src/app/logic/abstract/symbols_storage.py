from abc import ABC, abstractmethod
from typing import Optional


class SymbolsStorage(ABC):
    @abstractmethod
    async def get_price_or_none(self, symbol: str) -> Optional[float]:
        raise NotImplementedError
