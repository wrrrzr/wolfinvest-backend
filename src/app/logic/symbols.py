from typing import Optional

from .abstract import SymbolsPriceStorage


class GetSymbol:
    def __init__(self, symbols: SymbolsPriceStorage) -> None:
        self.symbols = symbols

    async def __call__(self, symbol: str) -> Optional[float]:
        return await self.symbols.get_price_or_none(symbol)
