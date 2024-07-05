from abc import ABC, abstractmethod

MAIN_CURRENCY = "USD"


class CurrencyPriceGetter(ABC):
    @abstractmethod
    async def get_price(self, currency: str) -> float:
        raise NotImplementedError


class CurrencyGetter(CurrencyPriceGetter, ABC):
    pass
