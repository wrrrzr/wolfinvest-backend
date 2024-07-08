from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models.symbol import SymbolAction


class SymbolsActionsAdder(ABC):
    @abstractmethod
    async def insert_buy(
        self, user_id: int, ticker: str, amount: int, created_at: datetime
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_sell(
        self, user_id: int, ticker: str, amount: int, created_at: datetime
    ) -> None:
        raise NotImplementedError


class SymbolsActionsManySelector(ABC):
    @abstractmethod
    async def get_all_user_symbols_actions(
        self, user_id: int
    ) -> list[SymbolAction]:
        raise NotImplementedError


class SymbolsActionsUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_symbols_actions(self, user_id: int) -> None:
        raise NotImplementedError


class SymbolsActionsStorage(
    SymbolsActionsAdder,
    SymbolsActionsManySelector,
    SymbolsActionsUsersDeletor,
    ABC,
):
    pass
