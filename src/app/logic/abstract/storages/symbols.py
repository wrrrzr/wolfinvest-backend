from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models.symbol import SymbolAction, UserSymbolData


class SymbolsAdder(ABC):
    @abstractmethod
    async def add(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        current_time: datetime,
    ) -> None:
        raise NotImplementedError


class SymbolsAmountSelector(ABC):
    @abstractmethod
    async def get_amount(self, user_id: int, ticker: str) -> int:
        raise NotImplementedError


class SymbolsManySelector(ABC):
    @abstractmethod
    async def get_all_user_symbols(
        self, user_id: int
    ) -> dict[str, UserSymbolData]:
        raise NotImplementedError


class SymbolsActionsManySelector(ABC):
    @abstractmethod
    async def get_user_symbols_actions_by_symbol(
        self, user_id: int, ticker: str
    ) -> list[SymbolAction]:
        raise NotImplementedError


class SymbolsRemover(ABC):
    @abstractmethod
    async def remove(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        current_time: datetime,
    ) -> None:
        raise NotImplementedError


class SymbolsUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_symbols(self, user_id: int) -> None:
        raise NotImplementedError


class SymbolsStorage(
    SymbolsAdder,
    SymbolsAmountSelector,
    SymbolsManySelector,
    SymbolsActionsManySelector,
    SymbolsRemover,
    SymbolsUsersDeletor,
    ABC,
):
    pass
