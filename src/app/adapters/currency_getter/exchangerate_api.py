import aiohttp

from app.logic.abstract.currency_getter import CurrencyGetter
from app.logic.abstract.storages.currency import MAIN_CURRENCY
from app.logic.exceptions import UnfoundCurrencyError


class ExchangerateApiGetter(CurrencyGetter):
    async def get_price(self, currency: str) -> float:
        if currency == MAIN_CURRENCY:
            return 1.0

        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        try:
            return data["rates"][MAIN_CURRENCY]
        except KeyError:
            raise UnfoundCurrencyError(f"Cannot find currency {currency}")
