from app.logic.abstract.currency_getter import CurrencyPriceGetter


class GetUserCurrencies:
    pass


class GetCurrencyPrice:
    def __init__(self, currency_price: CurrencyPriceGetter) -> None:
        self._currency_price = currency_price

    async def __call__(self, currency: str) -> float:
        return await self._currency_price.get_price(currency)
