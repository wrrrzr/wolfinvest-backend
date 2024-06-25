from abc import ABC, abstractmethod


class TickerFinder(ABC):
    @abstractmethod
    async def find_ticker(self, name: str) -> list[str]:
        raise NotImplementedError
