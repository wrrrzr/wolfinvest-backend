from app.logic.abstract import SymbolsGetter
from app.adapters.cache import SymbolsGetterCache, create_symbols_getter_memory

MOCK_SYMBOL_PRICE = 1.2
MOCK_SYMBOL_HISTORY = [1.2, 1.1, 1.1, 1.0, 1.1, 0.9]


class CounterSymbolsGetter(SymbolsGetter):
    def __init__(self) -> None:
        self.count_price = 0
        self.count_daily_history = 0

    async def get_price(self, symbol: str) -> float:
        self.count_price += 1
        return MOCK_SYMBOL_PRICE

    async def get_daily_history(self, symbol: str) -> list[float]:
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
