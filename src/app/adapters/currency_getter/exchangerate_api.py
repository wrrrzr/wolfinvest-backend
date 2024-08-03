import aiohttp

from app.logic.abstract.currency_getter import CurrencyGetter
from app.logic.abstract.currency_storage import MAIN_CURRENCY


class ExchangerateApiGetter(CurrencyGetter):
    async def get_price(self, currency: str) -> float:
        if currency == MAIN_CURRENCY:
            return 1.0

        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data["rates"][MAIN_CURRENCY]
