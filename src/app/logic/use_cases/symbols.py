from dataclasses import dataclass

from app.logic.abstract.ticker_finder import (
    TickerFinder,
)
from app.logic.abstract.symbols_getter import (
    SymbolsManyPriceGetter,
    SymbolsPriceGetter,
    SymbolsHistoryGetter,
)
from app.logic.abstract.symbols_storage import (
    SymbolsAdder,
    SymbolsManySelector,
    SymbolsActionsManySelector,
    SymbolsRemover,
    SymbolsAmountSelector,
)
from app.logic.abstract.currency_storage import (
    CurrencyRemover,
    CurrencyAmountSelector,
    CurrencyAdder,
)
from app.logic.abstract.transaction import Transaction
from app.logic.exceptions import NotEnoughBalanceError, NotEnoughSymbolsError
from app.logic.models import (
    SymbolHistory,
    SymbolPrice,
    SymbolTicker,
    SymbolHistoryInterval,
    SymbolData,
)
from app.logic.models.symbol import SymbolAction, Action


@dataclass
class Earn:
    absolute: float
    precent: float


def count_earn_symbol(
    actions: list[SymbolAction], current_amount: int, current_price: float
) -> Earn:
    total = 0.0

    for i in actions:
        if i.action == Action.buy:
            total -= i.price * i.amount
        elif i.action == Action.sell:
            total += i.price * i.amount

    total += current_price * current_amount
    return Earn(total, total / 100 * current_price / current_amount)


class GetSymbol:
    def __init__(
        self, symbols_getter: SymbolsPriceGetter, ticker_finder: TickerFinder
    ) -> None:
        self._symbols_getter = symbols_getter
        self._ticker_finder = ticker_finder

    async def __call__(self, symbol: str) -> SymbolData:
        symbol = symbol.upper()
        return SymbolData(
            price=await self._symbols_getter.get_price(symbol),
            name=await self._ticker_finder.get_name_by_ticker(symbol),
        )


class GetSymbolHistory:
    def __init__(self, symbols_getter: SymbolsHistoryGetter) -> None:
        self._symbols_getter = symbols_getter

    async def __call__(
        self, interval: SymbolHistoryInterval, symbol: str
    ) -> list[SymbolHistory]:
        symbol = symbol.upper()
        return await self._symbols_getter.get_history(interval, symbol)


class BuySymbol:
    def __init__(
        self,
        symbols_getter: SymbolsPriceGetter,
        symbols_adder: SymbolsAdder,
        currency_remover: CurrencyRemover,
        currency_amount: CurrencyAmountSelector,
        transaction: Transaction,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols_adder = symbols_adder
        self._currency_remover = currency_remover
        self._currency_amount = currency_amount
        self._transaction = transaction

    async def __call__(self, user_id: int, symbol: str, amount: int) -> None:
        symbol = symbol.upper()
        price = await self._symbols_getter.get_price(symbol)
        user_balance = await self._currency_amount.get_amount(
            user_id, price.currency
        )
        if user_balance < price.buy * amount:
            raise NotEnoughBalanceError()
        await self._currency_remover.remove(
            user_id, price.currency, price.buy * amount, 0.0
        )
        await self._symbols_adder.add(user_id, symbol, amount, price.buy)
        await self._transaction.commit()


@dataclass
class MySymbolDTO:
    name: str
    code: str
    amount: int
    price: SymbolPrice
    earn: Earn


class GetMySymbols:
    def __init__(
        self,
        symbols_many_selector: SymbolsManySelector,
        symbols_getter: SymbolsManyPriceGetter,
        ticker_finder: TickerFinder,
        symbols_actions: SymbolsActionsManySelector,
    ) -> None:
        self._symbols_many_selector = symbols_many_selector
        self._symbols_getter = symbols_getter
        self._ticker_finder = ticker_finder
        self._symbols_actions = symbols_actions

    async def __call__(self, user_id: int) -> list[MySymbolDTO]:
        symbols_res = await self._symbols_many_selector.get_all_user_symbols(
            user_id
        )
        symbols = {k: v for k, v in symbols_res.items() if v.amount > 0}
        res = []

        prices = await self._symbols_getter.get_many_prices(symbols.keys())

        for (ticker, symbol_data), price in zip(symbols.items(), prices):
            res.append(
                MySymbolDTO(
                    name=await self._ticker_finder.get_name_by_ticker(ticker),
                    code=ticker,
                    amount=symbol_data.amount,
                    price=price,
                    earn=count_earn_symbol(
                        symbol_data.actions, symbol_data.amount, price.buy
                    ),
                )
            )
        return res


class SellSymbol:
    def __init__(
        self,
        symbols_getter: SymbolsPriceGetter,
        symbols_remover: SymbolsRemover,
        symbols_amount_selector: SymbolsAmountSelector,
        currency_adder: CurrencyAdder,
        transaction: Transaction,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols_remover = symbols_remover
        self._symbols_amount_selector = symbols_amount_selector
        self._currency_adder = currency_adder
        self._transaction = transaction

    async def __call__(self, user_id: int, symbol: str, amount: int) -> None:
        symbol = symbol.upper()
        user_amount = await self._symbols_amount_selector.get_amount(
            user_id, symbol
        )
        if user_amount < amount:
            raise NotEnoughSymbolsError()
        price = await self._symbols_getter.get_price(symbol)
        await self._symbols_remover.remove(user_id, symbol, amount, price.sell)
        await self._currency_adder.add(
            user_id, price.currency, price.sell * amount, 0.0
        )
        await self._transaction.commit()


class FindTicker:
    def __init__(self, ticker_finder: TickerFinder) -> None:
        self._ticker_finder = ticker_finder

    async def __call__(self, name: str) -> list[SymbolTicker]:
        return await self._ticker_finder.find_ticker(name)
