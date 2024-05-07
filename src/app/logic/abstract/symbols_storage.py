from abc import ABC, abstractmethod

from app.logic.models import Symbol


class SymbolsStorage(ABC):
    @abstractmethod
    async def insert_or_add(
        self, owner_id: int, code: str, amount: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_amount(self, owner_id: int, code: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_user_symbols(self, user_id: int) -> list[Symbol]:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, owner_id: int, code: str, amount: int) -> None:
        raise NotImplementedError
