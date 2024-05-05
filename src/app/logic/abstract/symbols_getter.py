from abc import ABC, abstractmethod


class SymbolsGetter(ABC):
    @abstractmethod
    async def get_price(self, symbol: str) -> float:
        raise NotImplementedError
