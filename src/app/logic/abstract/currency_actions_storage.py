from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models.currency import CurrencyAction


class CurrencyActionsAdder(ABC):
    @abstractmethod
    async def insert_buy(
        self,
        user_id: int,
        ticker: str,
        amount: float,
        price: float,
        created_at: datetime,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_sell(
        self,
        user_id: int,
        ticker: str,
        amount: float,
        price: float,
        created_at: datetime,
    ) -> None:
        raise NotImplementedError


class CurrencyActionsManySelector(ABC):
    @abstractmethod
    async def get_user_currencies_actions_by_currency(
        self, user_id: int, ticker: str
    ) -> list[CurrencyAction]:
        raise NotImplementedError


class CurrencyActionsUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_currency_actions(self, user_id: int) -> None:
        raise NotImplementedError


class CurrencyActionsStorage(
    CurrencyActionsAdder,
    CurrencyActionsManySelector,
    CurrencyActionsUsersDeletor,
    ABC,
):
    pass
