import json

from app.logic.abstract import TickerFinder
from app.logic.models import SymbolTicker
from app.config import load_tickers_config

FILE_PATH = load_tickers_config().file_path

with open(FILE_PATH, "r", encoding="utf-8") as f:
    TICKERS_KV = json.load(f)


class TickersFileTickerFinder(TickerFinder):
    async def find_ticker(self, name: str) -> list[SymbolTicker]:
        name = name.lower()
        res = []
        count = 0
        for k, v in TICKERS_KV.items():
            if name in k:
                res.append(SymbolTicker(name=k, ticker=v))
                count += 1
            if count >= 5:
                break
        return res

    async def get_name_by_ticker(self, ticker: str) -> str:
        ticker = ticker.upper()
        for k, v in TICKERS_KV.items():
            if v == ticker:
                return k
