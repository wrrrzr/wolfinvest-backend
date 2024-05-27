from app.logic.abstract import SymbolsList
from app.logic.models import SymbolInList


class StaticSymbolsList(SymbolsList):
    async def get_all(self) -> list[SymbolInList]:
        return [
            SymbolInList(code="MSFT", name="Microsoft"),
            SymbolInList(code="AAPL", name="Apple"),
            SymbolInList(code="NVDA", name="Nvidia"),
            SymbolInList(code="GOOGL", name="Google"),
            SymbolInList(code="AMZN", name="Amazon"),
            SymbolInList(code="META", name="Meta"),
            SymbolInList(code="TSLA", name="Tesla"),
            SymbolInList(code="V", name="Visa"),
            SymbolInList(code="OCRL", name="Oracle"),
            SymbolInList(code="NFLX", name="Netflix"),
            SymbolInList(code="OR", name="L'Oreal"),
            SymbolInList(code="MCD", name="McDonal's"),
            SymbolInList(code="UBER", name="Uber"),
        ]
