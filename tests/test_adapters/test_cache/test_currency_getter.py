import pytest

from app.adapters.cache import (
    CacheCurrencyGetter,
    create_currency_getter_memory,
)
from app.logic.abstract.currency_getter import CurrencyGetter

MOCK_PRICE = 1.6


class CurrencyGetterCounter(CurrencyGetter):
    def __init__(self) -> None:
        self.count_price = 0

    async def get_price(self, currency: str) -> float:
        self.count_price += 1
        return MOCK_PRICE


@pytest.fixture
def target() -> tuple[CacheCurrencyGetter, CurrencyGetterCounter]:
    counter = CurrencyGetterCounter()
    getter = CacheCurrencyGetter(counter, create_currency_getter_memory())
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
