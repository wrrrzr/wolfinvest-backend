from abc import ABC, abstractmethod

from app.logic.models import Symbol


class SymbolsAdder(ABC):
    @abstractmethod
    async def insert_or_add(
        self, owner_id: int, code: str, amount: int
    ) -> None:
        raise NotImplementedError


class SymbolsAmountSelector(ABC):
    @abstractmethod
    async def get_amount(self, owner_id: int, code: str) -> int:
        raise NotImplementedError


class SymbolsManySelector(ABC):
    @abstractmethod
    async def get_all_user_symbols(self, user_id: int) -> list[Symbol]:
        raise NotImplementedError


class SymbolsRemover(ABC):
    @abstractmethod
    async def remove(self, owner_id: int, code: str, amount: int) -> None:
        raise NotImplementedError


class SymbolsUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_symbols(self, user_id: int) -> None:
        raise NotImplementedError


class SymbolsStorage(
    SymbolsAdder,
    SymbolsAmountSelector,
    SymbolsManySelector,
    SymbolsRemover,
    SymbolsUsersDeletor,
    ABC,
):
    pass
