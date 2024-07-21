from abc import ABC, abstractmethod

from app.logic.models.currency import Currency


class CurrencyUserAllSelector(ABC):
    @abstractmethod
    async def get_all_user_currencies(self, user_id: int) -> list[Currency]:
        raise NotImplementedError


class CurrencyStorage(CurrencyUserAllSelector, ABC):
    pass
