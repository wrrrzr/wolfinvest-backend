from app.logic.abstract.currency_getter import CurrencyPriceGetter
from app.logic.abstract.currency_storage import CurrencyUserAllSelector
from app.logic.models.currency import Currency


class GetUserCurrencies:
    def __init__(self, currency_storage: CurrencyUserAllSelector) -> None:
        self._currency_storage = currency_storage

    async def __call__(self, user_id: int) -> list[Currency]:
        return await self._currency_storage.get_all_user_currencies(user_id)


class GetCurrencyPrice:
    def __init__(self, currency_price: CurrencyPriceGetter) -> None:
        self._currency_price = currency_price

    async def __call__(self, currency: str) -> float:
        return await self._currency_price.get_price(currency)
