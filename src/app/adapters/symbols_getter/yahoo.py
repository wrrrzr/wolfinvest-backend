from datetime import datetime

import aiohttp

from app.logic.abstract import SymbolsPriceGetter, SymbolsHistoryGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory, SymbolPrice


class YahooSymbolsGetter(SymbolsPriceGetter, SymbolsHistoryGetter):
    async def get_price(self, symbol: str) -> SymbolPrice:
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
                            price=SymbolPrice(buy=i[0], sell=i[1]),
                            timestamp=datetime.fromtimestamp(i[2]),
                        )
                        for i in zip(
                            resp["indicators"]["quote"][-1]["high"],
                            resp["indicators"]["quote"][-1]["low"],
                            resp["timestamp"],
                        )
                    ]
        except (TypeError, KeyError):
            raise UnfoundSymbolError()
