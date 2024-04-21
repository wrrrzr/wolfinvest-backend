from typing import Optional

from yahoo_finance_async import OHLC
from yahoo_finance_async.api import APIError

from app.logic.abstract import SymbolsPriceStorage


class YahooSymbolsPriceStorage(SymbolsPriceStorage):
    async def get_price_or_none(self, symbol: str) -> Optional[float]:
        try:
            return (await OHLC.fetch(symbol))["candles"][-1]["open"]
        except APIError:
            return None
