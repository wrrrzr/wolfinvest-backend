import asyncio
from datetime import datetime
from dataclasses import dataclass
from typing import Iterable

import aiohttp

from app.logic.abstract.symbols_getter import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory, SymbolPrice, SymbolHistoryInterval


@dataclass
class YahooHistoryData:
    interval: str
    history: str


SYMBOLS_HISTORY_INTERVALS_YAHOO = {
    SymbolHistoryInterval.FIVE_MINUTES: YahooHistoryData("5m", "1d"),
    SymbolHistoryInterval.HOUR: YahooHistoryData("1h", "1wk"),
    SymbolHistoryInterval.DAY: YahooHistoryData("1d", "1mo"),
    SymbolHistoryInterval.WEEK: YahooHistoryData("1wk", "3mo"),
    SymbolHistoryInterval.MONTH: YahooHistoryData("1mo", "5y"),
    SymbolHistoryInterval.THREE_MONTHS: YahooHistoryData("3mo", "max"),
}


class YahooSymbolsGetter(SymbolsGetter):
    async def get_price(self, symbol: str) -> SymbolPrice:
        return (
            await self.get_history(SymbolHistoryInterval.FIVE_MINUTES, symbol)
        )[0].price

    async def get_many_prices(
        self, symbols: Iterable[str]
    ) -> list[SymbolPrice]:
        price_tasks = [self.get_price(i) for i in symbols]
        return await asyncio.gather(*price_tasks)

    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        try:
            history_data = SYMBOLS_HISTORY_INTERVALS_YAHOO[interval]
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    params={
                        "events": "history",
                        "interval": history_data.interval,
                        "range": history_data.history,
                    },
                ) as resp:
                    resp = await resp.json()
                    resp = resp["chart"]["result"][0]
                    return [
                        SymbolHistory(
                            price=SymbolPrice(
                                buy=i[0],
                                sell=i[1],
                                currency=resp["meta"]["currency"],
                            ),
                            timestamp=datetime.fromtimestamp(i[2]),
                        )
                        for i in zip(
                            resp["indicators"]["quote"][-1]["high"],
                            resp["indicators"]["quote"][-1]["low"],
                            resp["timestamp"],
                        )
                    ]
        except (TypeError, KeyError):
            raise UnfoundSymbolError(f"Cannot find symbol {symbol}")
