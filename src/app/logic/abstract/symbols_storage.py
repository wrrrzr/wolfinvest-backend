from abc import ABC, abstractmethod

from app.logic.models import Symbol


class SymbolsStorage(ABC):
    @abstractmethod
    async def insert_or_add(
        self, owner_id: int, symbol: str, amount: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_user_symbols(self, user_id: int) -> list[Symbol]:
        raise NotImplementedError
