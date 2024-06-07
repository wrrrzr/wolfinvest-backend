from datetime import datetime

import aiohttp

from app.logic.abstract import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory


class YahooSymbolsGetter(SymbolsGetter):
    async def get_price(self, symbol: str) -> float:
        return (await self.get_daily_history(symbol))[0].price

    async def get_daily_history(self, symbol: str) -> list[SymbolHistory]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                    params={
                        "events": "history",
                        "interval": "30m",
                        "history": "1d",
                    },
                ) as resp:
                    resp = await resp.json()
                    resp = resp["chart"]["result"][0]
                    return [
                        SymbolHistory(
                            price=i[0], timestamp=datetime.fromtimestamp(i[1])
                        )
                        for i in zip(
                            resp["indicators"]["quote"][-1]["close"],
                            resp["timestamp"],
                        )
                    ]
        except (TypeError, KeyError):
            raise UnfoundSymbolError()
