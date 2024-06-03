import aiohttp

from app.logic.abstract import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError


class YahooSymbolsGetter(SymbolsGetter):
    async def get_price(self, symbol: str) -> float:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                    params={
                        "events": "history",
                        "interval": "5m",
                        "history": "1d",
                    },
                ) as resp:
                    return (await resp.json())["chart"]["result"][0][
                        "indicators"
                    ]["quote"][-1]["close"][0]
        except TypeError:
            raise UnfoundSymbolError()
