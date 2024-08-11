import json
from typing import Iterable

import aiofiles

from app.logic.abstract.ticker_finder import TickerFinder
from app.logic.models import SymbolTicker, TickersConfig


class TickersFileTickerFinder(TickerFinder):
    def __init__(self, config: TickersConfig) -> None:
        self._config = config

    async def find_ticker(self, name: str) -> list[SymbolTicker]:
        tickers_kv = await self._get_tickers_kv()

        name = name.lower()
        res = []
        count = 0
        for k, v in tickers_kv.items():
            if name in v:
                res.append(SymbolTicker(name=v, ticker=k))
                count += 1
            if count >= 5:
                break
        return res

    async def get_name_by_ticker(self, ticker: str) -> str:
        tickers_kv = await self._get_tickers_kv()
        ticker = ticker.upper()
        return tickers_kv.get(ticker, "???")

    async def get_names_by_tickers(self, tickers: Iterable[str]) -> list[str]:
        tickers_kv = await self._get_tickers_kv()
        return [tickers_kv[i] for i in tickers]

    async def _get_tickers_kv(self) -> dict[str, str]:
        file_path = self._config.file_path

        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            return json.loads(await f.read())
