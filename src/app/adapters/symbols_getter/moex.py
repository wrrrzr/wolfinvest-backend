import asyncio
from datetime import datetime, timedelta
from enum import IntEnum
from typing import Iterable

import aiohttp

from app.logic.abstract.symbols_getter import SymbolsGetter
from app.logic.exceptions import UnfoundSymbolError
from app.logic.models import SymbolHistory, SymbolPrice, SymbolHistoryInterval
from app.utils.funcs import get_current_time

MOEX_CURRENCY = "RUB"
AMOUNT_HISTORY = 100

SYMBOLS_HISTORY_INTERVALS_MOEX = {
    SymbolHistoryInterval.FIVE_MINUTES: 1,
    SymbolHistoryInterval.HOUR: 60,
    SymbolHistoryInterval.DAY: 24,
    SymbolHistoryInterval.WEEK: 7,
    SymbolHistoryInterval.MONTH: 31,
    SymbolHistoryInterval.THREE_MONTHS: 31,
}


class Columns(IntEnum):
    open = 0
    close = 1
    high = 2
    low = 3
    value = 4
    volume = 5
    begin = 6
    end = 7


def from_date_interval(interval: timedelta) -> str:
    return (get_current_time() - interval * AMOUNT_HISTORY).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def calc_from_date(interval: SymbolHistoryInterval) -> str:
    match interval:
        case SymbolHistoryInterval.FIVE_MINUTES:
            return from_date_interval(timedelta(minutes=1))
        case SymbolHistoryInterval.HOUR:
            return from_date_interval(timedelta(hours=1))
        case SymbolHistoryInterval.DAY:
            return from_date_interval(timedelta(days=1))
        case SymbolHistoryInterval.WEEK:
            return from_date_interval(timedelta(weeks=1))
        case SymbolHistoryInterval.MONTH:
            return from_date_interval(timedelta(days=31))
        case SymbolHistoryInterval.THREE_MONTHS:
            return from_date_interval(timedelta(days=90))
    raise ValueError("Unknown interval")


def calc_till_date(interval: SymbolHistoryInterval) -> str:
    return get_current_time().strftime("%Y-%m-%d %H:%M:%S")


class MoexSymbolsGetter(SymbolsGetter):
    async def get_price(self, symbol: str) -> SymbolPrice:
        return (
            await self.get_history(SymbolHistoryInterval.FIVE_MINUTES, symbol)
        )[0].price

    async def get_many_prices(
        self, symbols: Iterable[str]
    ) -> list[SymbolPrice]:
        price_tasks = [self.get_price(i) for i in symbols]
        return await asyncio.gather(*price_tasks)

    async def get_history(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        history_data = SYMBOLS_HISTORY_INTERVALS_MOEX[interval]
        url = (
            "https://iss.moex.com/"
            + "iss/engines/stock/markets/shares/securities/"
            + f"{symbol}/candles.json"
            + f"?from={calc_from_date(interval)}&till={calc_till_date(interval)}"
            + f"&interval={history_data}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp = (await resp.json())["candles"]["data"]

        if not resp:
            raise UnfoundSymbolError(f"Cannot find symbol {symbol}")

        return [
            SymbolHistory(
                price=SymbolPrice(
                    buy=i[Columns.high],
                    sell=i[Columns.low],
                    currency=MOEX_CURRENCY,
                ),
                timestamp=datetime.strptime(
                    i[Columns.end], "%Y-%m-%d %H:%M:%S"
                ),
            )
            for i in resp
        ]
