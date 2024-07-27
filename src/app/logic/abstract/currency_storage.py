from abc import ABC, abstractmethod

from app.logic.models.currency import CurrencyAction


class CurrencyUserAllSelector(ABC):
    @abstractmethod
    async def get_all_user_currencies(self, user_id: int) -> dict[str, float]:
        raise NotImplementedError


class CurrencyAmountSelector(ABC):
    @abstractmethod
    async def get_amount(self, user_id: int, ticker: str) -> float:
        raise NotImplementedError


class CurrencyAdder(ABC):
    @abstractmethod
    async def add(
        self, user_id: int, ticker: str, amount: float, price: float
    ) -> None:
        raise NotImplementedError


class CurrencyRemover(ABC):
    @abstractmethod
    async def remove(
        self, user_id: int, ticker: str, amount: float, price: float
    ) -> None:
        raise NotImplementedError


class CurrencyActionsManySelector(ABC):
    @abstractmethod
    async def get_user_currencies_actions_by_currency(
        self, user_id: int, ticker: str
    ) -> list[CurrencyAction]:
        raise NotImplementedError


class CurrencyUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_currencies(self, user_id: int) -> None:
        raise NotImplementedError


class CurrencyStorage(
    CurrencyUserAllSelector,
    CurrencyAmountSelector,
    CurrencyAdder,
    CurrencyRemover,
    CurrencyActionsManySelector,
    CurrencyUsersDeletor,
    ABC,
):
    pass
