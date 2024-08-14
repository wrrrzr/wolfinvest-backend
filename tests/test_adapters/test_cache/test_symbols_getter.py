from typing import Iterable

import pytest

from app.logic.abstract.symbols_getter import SymbolsGetter
from app.logic.models import SymbolHistory, SymbolPrice, SymbolHistoryInterval
from app.adapters.symbols_getter.memory_cache import MemoryCacheSymbolsGetter
from app.utils.funcs import get_current_time

MOCK_CURRENCY = "USD"
MOCK_SYMBOL_PRICE = SymbolPrice(1.2, 1.0, MOCK_CURRENCY)
MOCK_SYMBOL_HISTORY = {
    SymbolHistoryInterval.FIVE_MINUTES: [
        SymbolHistory(
            SymbolPrice(1.2, 1.0, MOCK_CURRENCY), get_current_time()
        ),
        SymbolHistory(
            SymbolPrice(1.1, 1.0, MOCK_CURRENCY), get_current_time()
        ),
        SymbolHistory(
            SymbolPrice(1.1, 1.0, MOCK_CURRENCY), get_current_time()
        ),
        SymbolHistory(
            SymbolPrice(1.0, 0.9, MOCK_CURRENCY), get_current_time()
        ),
        SymbolHistory(
            SymbolPrice(1.1, 1.0, MOCK_CURRENCY), get_current_time()
        ),
        SymbolHistory(
            SymbolPrice(0.9, 0.8, MOCK_CURRENCY), get_current_time()
        ),
    ]
}


class CounterSymbolsGetter(SymbolsGetter):
    def __init__(self) -> None:
        self.count_price = 0
        self.count_history = 0

    async def get_price(self, symbol: str) -> SymbolPrice:
        self.count_price += 1
        return MOCK_SYMBOL_PRICE

    async def get_many_prices(
        self, symbols: Iterable[str]
    ) -> list[SymbolPrice]:
        raise AssertionError(
            "MemoryCacheSymbolsGetter do not called inner get_many_prices"
        )

    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        self.count_history += 1
        return MOCK_SYMBOL_HISTORY[interval]


@pytest.fixture
def target() -> tuple[MemoryCacheSymbolsGetter, CounterSymbolsGetter]:
    counter = CounterSymbolsGetter()
    getter = MemoryCacheSymbolsGetter(
        counter, MemoryCacheSymbolsGetter.create_memory()
    )
    return getter, counter


async def test_get_price(target) -> None:
    getter, counter = target
    assert await getter.get_price("AAPL") == MOCK_SYMBOL_PRICE


async def test_get_price_caching(target) -> None:
    getter, counter = target
    await getter.get_price("AAPL")
    await getter.get_price("AAPL")
    await getter.get_price("AAPL")
    assert counter.count_price == 1


async def test_get_price_caching_many(target) -> None:
    getter, counter = target
    await getter.get_price("AAPL")
    await getter.get_price("MSFT")
    await getter.get_price("AAPL")
    assert counter.count_price == 2


async def test_get_history(target) -> None:
    getter, counter = target
    assert (
        await getter.get_history(SymbolHistoryInterval.FIVE_MINUTES, "AAPL")
        == MOCK_SYMBOL_HISTORY[SymbolHistoryInterval.FIVE_MINUTES]
    )


async def test_get_history_caching(target) -> None:
    getter, counter = target
    await getter.get_history(SymbolHistoryInterval.FIVE_MINUTES, "AAPL")
    await getter.get_history(SymbolHistoryInterval.FIVE_MINUTES, "AAPL")
    assert counter.count_history == 1


async def test_get_history_caching_many(target) -> None:
    getter, counter = target
    await getter.get_history(SymbolHistoryInterval.FIVE_MINUTES, "AAPL")
    await getter.get_history(SymbolHistoryInterval.FIVE_MINUTES, "MSFT")
    await getter.get_history(SymbolHistoryInterval.FIVE_MINUTES, "AAPL")
    assert counter.count_history == 2


async def test_get_many_prices(target) -> None:
    getter, counter = target
    await getter.get_many_prices(["AMZN", "AAPL", "MSFT"])
    assert counter.count_price == 3


async def test_cache_get_many_prices(target) -> None:
    getter, counter = target
    await getter.get_many_prices(["AMZN", "AAPL", "MSFT"])
    await getter.get_many_prices(["AAPL", "MSFT", "GOOGL"])
    await getter.get_price("AMZN")
    assert counter.count_price == 4
