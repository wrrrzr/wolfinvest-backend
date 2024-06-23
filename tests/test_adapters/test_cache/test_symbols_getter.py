from app.logic.abstract import SymbolsGetter
from app.logic.models import SymbolHistory, SymbolPrice
from app.adapters.cache import SymbolsGetterCache, create_symbols_getter_memory
from app.utils.funcs import get_current_time

MOCK_SYMBOL_PRICE = SymbolPrice(1.2, 1.0)
MOCK_SYMBOL_HISTORY = [
    SymbolHistory(SymbolPrice(1.2, 1.0), get_current_time()),
    SymbolHistory(SymbolPrice(1.1, 1.0), get_current_time()),
    SymbolHistory(SymbolPrice(1.1, 1.0), get_current_time()),
    SymbolHistory(SymbolPrice(1.0, 0.9), get_current_time()),
    SymbolHistory(SymbolPrice(1.1, 1.0), get_current_time()),
    SymbolHistory(SymbolPrice(0.9, 0.8), get_current_time()),
]


class CounterSymbolsGetter(SymbolsGetter):
    def __init__(self) -> None:
        self.count_price = 0
        self.count_daily_history = 0

    async def get_price(self, symbol: str) -> SymbolPrice:
        self.count_price += 1
        return MOCK_SYMBOL_PRICE

    async def get_daily_history(self, symbol: str) -> list[SymbolHistory]:
        self.count_daily_history += 1
        return MOCK_SYMBOL_HISTORY


async def test_get_price() -> None:
    getter = SymbolsGetterCache(
        CounterSymbolsGetter(), create_symbols_getter_memory()
    )
    assert await getter.get_price("AAPL") == MOCK_SYMBOL_PRICE


async def test_get_price_caching() -> None:
    counter = CounterSymbolsGetter()
    getter = SymbolsGetterCache(counter, create_symbols_getter_memory())
    await getter.get_price("AAPL")
    await getter.get_price("AAPL")
    await getter.get_price("AAPL")
    assert counter.count_price == 1


async def test_get_price_caching_many() -> None:
    counter = CounterSymbolsGetter()
    getter = SymbolsGetterCache(counter, create_symbols_getter_memory())
    await getter.get_price("AAPL")
    await getter.get_price("MSFT")
    await getter.get_price("AAPL")
    assert counter.count_price == 2


async def test_get_daily_history() -> None:
    getter = SymbolsGetterCache(
        CounterSymbolsGetter(), create_symbols_getter_memory()
    )
    assert await getter.get_daily_history("AAPL") == MOCK_SYMBOL_HISTORY


async def test_get_daily_history_caching() -> None:
    counter = CounterSymbolsGetter()
    getter = SymbolsGetterCache(counter, create_symbols_getter_memory())
    await getter.get_daily_history("AAPL")
    await getter.get_daily_history("AAPL")
    assert counter.count_daily_history == 1


async def test_get_daily_history_caching_many() -> None:
    counter = CounterSymbolsGetter()
    getter = SymbolsGetterCache(counter, create_symbols_getter_memory())
    await getter.get_daily_history("AAPL")
    await getter.get_daily_history("MSFT")
    await getter.get_daily_history("AAPL")
    assert counter.count_daily_history == 2
