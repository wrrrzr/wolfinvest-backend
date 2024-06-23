from app.logic.abstract import SymbolsList
from app.logic.models import SymbolInList, SymbolPrice
from app.adapters.cache import SymbolsListCache, create_symbols_list_memory


MOCK_SYMBOLS_LIST = [
    SymbolInList(
        code="MSFT", name="Microsoft", price=SymbolPrice(100.0, 99.9)
    ),
    SymbolInList(code="AAPL", name="Apple", price=SymbolPrice(212.5, 212.0)),
]


class CounterSymbolsList(SymbolsList):
    def __init__(self) -> None:
        self.count = 0

    async def get_all(self) -> list[SymbolInList]:
        self.count += 1
        return MOCK_SYMBOLS_LIST


async def test_get_all() -> None:
    counter = CounterSymbolsList()
    symbols_list = SymbolsListCache(counter, create_symbols_list_memory())
    await symbols_list.get_all()
    await symbols_list.get_all()
    data = await symbols_list.get_all()
    assert counter.count == 1
    assert data == MOCK_SYMBOLS_LIST
