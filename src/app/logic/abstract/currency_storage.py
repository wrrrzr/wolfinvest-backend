from abc import ABC, abstractmethod

from app.logic.models.currency import Currency


class CurrencyUserAllSelector(ABC):
    @abstractmethod
    async def get_all_user_currencies(self, user_id: int) -> list[Currency]:
        raise NotImplementedError


class CurrencyAdder(ABC):
    @abstractmethod
    async def insert_or_add(
        self, user_id: int, ticker: str, amount: float
    ) -> None:
        raise NotImplementedError


class CurrencyUsersDeletor(ABC):
    @abstractmethod
    async def delete_all_user_currencies(self, user_id: int) -> None:
        raise NotImplementedError


class CurrencyStorage(
    CurrencyUserAllSelector, CurrencyAdder, CurrencyUsersDeletor, ABC
):
    pass
