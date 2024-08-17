import asyncio
from collections import defaultdict
from datetime import timedelta, datetime
from dataclasses import dataclass

from app.logic.abstract.currency_getter import CurrencyGetter
from app.logic.abstract.clock import ClockCurrentTimeGetter

TIME_EXP_PRICE = timedelta(minutes=10)


@dataclass
class CachedCurrencyPrice:
    price: float
    time_exp_cache: datetime


@dataclass
class MemoryCurrencyGetter:
    price: dict[str, CachedCurrencyPrice]
    locks: dict[str, asyncio.Lock]


class MemoryCacheCurrencyGetter(CurrencyGetter):
    def __init__(
        self,
        inner: CurrencyGetter,
        memory: MemoryCurrencyGetter,
        clock: ClockCurrentTimeGetter,
    ) -> None:
        self._inner = inner
        self._memory = memory
        self._clock = clock

    @staticmethod
    def create_memory() -> MemoryCurrencyGetter:
        return MemoryCurrencyGetter({}, defaultdict(asyncio.Lock))

    async def get_price(self, currency: str) -> float:
        async with self._memory.locks[currency]:
            if currency not in self._memory.price:
                await self._add_to_cache(currency)
            if (
                self._memory.price[currency].time_exp_cache
                < await self._clock.get_current_time()
            ):
                await self._add_to_cache(currency)
            return self._memory.price[currency].price

    async def _add_to_cache(self, currency: str) -> None:
        self._memory.price[currency] = CachedCurrencyPrice(
            await self._inner.get_price(currency),
            TIME_EXP_PRICE + await self._clock.get_current_time(),
        )
