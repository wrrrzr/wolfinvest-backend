import aiohttp

from app.logic.abstract.currency_getter import CurrencyGetter, MAIN_CURRENCY


class ExchangerateApiGetter(CurrencyGetter):
    async def get_price(self, currency: str) -> float:
        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data["rates"][MAIN_CURRENCY]
