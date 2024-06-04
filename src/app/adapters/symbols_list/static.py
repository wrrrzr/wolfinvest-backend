from dataclasses import dataclass

from app.logic.abstract import SymbolsGetter, SymbolsList
from app.logic.models import SymbolInList


@dataclass
class StaticSymbol:
    code: str
    name: str


_data = [
    StaticSymbol(code="MSFT", name="Microsoft"),
    StaticSymbol(code="AAPL", name="Apple"),
    StaticSymbol(code="NVDA", name="Nvidia"),
    StaticSymbol(code="GOOGL", name="Google"),
    StaticSymbol(code="AMZN", name="Amazon"),
    StaticSymbol(code="META", name="Meta"),
    StaticSymbol(code="TSLA", name="Tesla"),
    StaticSymbol(code="V", name="Visa"),
    StaticSymbol(code="NFLX", name="Netflix"),
    StaticSymbol(code="OR", name="L'Oreal"),
    StaticSymbol(code="MCD", name="McDonal's"),
    StaticSymbol(code="UBER", name="Uber"),
]


class StaticSymbolsList(SymbolsList):
    def __init__(self, symbols_getter: SymbolsGetter) -> None:
        self._symbols_getter = symbols_getter

    async def get_all(self) -> list[SymbolInList]:
        return [
            SymbolInList(
                code=i.code,
                name=i.name,
                price=await self._symbols_getter.get_price(i.code),
            )
            for i in _data
        ]
