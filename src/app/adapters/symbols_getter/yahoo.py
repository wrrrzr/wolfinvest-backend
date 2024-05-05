from yahoo_finance_async import OHLC
from yahoo_finance_async.api import APIError

from app.logic.abstract import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError


class YahooSymbolsGetter(SymbolsGetter):
    async def get_price(self, symbol: str) -> float:
        try:
            return (await OHLC.fetch(symbol))["candles"][-1]["open"]
        except APIError:
            raise UnfoundSymbolError()
