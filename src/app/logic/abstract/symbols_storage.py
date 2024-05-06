from abc import ABC, abstractmethod


class SymbolsStorage(ABC):
    @abstractmethod
    async def insert_or_add(
        self, user_id: int, symbol: str, amount: int
    ) -> None:
        raise NotImplementedError
