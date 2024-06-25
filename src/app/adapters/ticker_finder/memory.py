from app.logic.abstract import TickerFinder
from app.logic.models import SymbolTicker

TICKERS_KV = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "nvidia": "NVDA",
    "google": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "eli lilly": "LLY",
    "broadcom": "AVGO",
    "tesla": "TSLA",
    "jp morgan chase": "JPM",
    "visa": "V",
    "walmart": "WMT",
    "exxon mobi": "XOM",
    "unitedhealth group": "UNH",
    "mastercard": "MA",
    "procter & gamble": "PG",
    "oracle": "ORCL",
    "costco wholesale": "COST",
    "netflix": "NFLX",
    "cocacola": "KO",
    "amd": "AMD",
    "adobe": "ADBE",
    "uber": "UBER",
    "nike": "NIKE",
    "paypal": "PYPL",
}


class MemoryTickerFinder(TickerFinder):
    async def find_ticker(self, name: str) -> list[SymbolTicker]:
        name = name.lower()
        return [
            SymbolTicker(name=k, ticker=v)
            for k, v in TICKERS_KV.items()
            if name in k
        ]
