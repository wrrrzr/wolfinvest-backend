import asyncio
from datetime import datetime, timezone, timedelta

import pytest

from app.adapters.currency_getter import MemoryCacheCurrencyGetter
from app.adapters.clock import UTCClock
from app.logic.abstract.currency_getter import CurrencyGetter

MOCK_PRICE = 1.6


class CurrencyGetterCounter(CurrencyGetter):
    def __init__(self) -> None:
        self.count_price = 0

    async def get_price(self, currency: str) -> float:
        self.count_price += 1
        return MOCK_PRICE


@pytest.fixture
def target() -> tuple[MemoryCacheCurrencyGetter, CurrencyGetterCounter]:
    counter = CurrencyGetterCounter()
    getter = MemoryCacheCurrencyGetter(
        counter,
        MemoryCacheCurrencyGetter.create_memory(),
        UTCClock(),
    )
    return getter, counter


async def test_get_price(target) -> None:
    getter, counter = target
    assert await getter.get_price("EUR") == MOCK_PRICE


async def test_get_price_caching(target) -> None:
    getter, counter = target
    await getter.get_price("EUR")
    await getter.get_price("EUR")
    await getter.get_price("EUR")
    assert counter.count_price == 1


async def test_get_price_caching_many(target) -> None:
    getter, counter = target
    await getter.get_price("EUR")
    await getter.get_price("CAD")
    await getter.get_price("EUR")
    assert counter.count_price == 2


class SlowCounter(CurrencyGetter):
    def __init__(self) -> None:
        self.count_price = 0

    async def get_price(self, currency: str) -> float:
        self.count_price += 1
        await asyncio.sleep(0.25)
        return MOCK_PRICE


async def test_get_price_slow_service() -> None:
    slow_counter = SlowCounter()
    getter = MemoryCacheCurrencyGetter(
        slow_counter, MemoryCacheCurrencyGetter.create_memory(), UTCClock()
    )

    await asyncio.gather(
        getter.get_price("EUR"),
        getter.get_price("EUR"),
        getter.get_price("CNY"),
        getter.get_price("EUR"),
    )
    assert slow_counter.count_price == 2


async def test_get_price_slow_service_speed() -> None:
    slow_counter = SlowCounter()
    getter = MemoryCacheCurrencyGetter(
        slow_counter, MemoryCacheCurrencyGetter.create_memory(), UTCClock()
    )

    time = datetime.now(timezone.utc)
    await asyncio.gather(
        getter.get_price("USD"),
        getter.get_price("CNY"),
        getter.get_price("RUB"),
        getter.get_price("EUR"),
    )
    assert time + timedelta(seconds=0.5) > datetime.now(timezone.utc)
