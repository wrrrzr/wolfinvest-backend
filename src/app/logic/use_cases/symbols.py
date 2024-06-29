from dataclasses import dataclass

from app.logic.abstract import (
    SymbolsPriceGetter,
    SymbolsHistoryGetter,
    UsersOneSelector,
    SymbolsStorage,
    TickerFinder,
)
from app.logic.exceptions import NotEnoughBalanceError, NotEnoughSymbolsError
from app.logic.models import (
    SymbolHistory,
    SymbolPrice,
    SymbolTicker,
    SymbolHistoryInterval,
    BalanceChangeReason,
)
from app.logic.balance_editor import BalanceEditor


class GetSymbol:
    def __init__(self, symbols_getter: SymbolsPriceGetter) -> None:
        self._symbols_getter = symbols_getter

    async def __call__(self, symbol: str) -> SymbolPrice:
        symbol = symbol.upper()
        return await self._symbols_getter.get_price(symbol)


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
        symbols: SymbolsStorage,
        users: UsersOneSelector,
        users_balance: BalanceEditor,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols = symbols
        self._users = users
        self._users_balance = users_balance

    async def __call__(self, user_id: int, symbol: str, amount: int) -> float:
        symbol = symbol.upper()
        price = (await self._symbols_getter.get_price(symbol)).buy
        user = await self._users.select_one_by_id(user_id)
        if user.balance < price * amount:
            raise NotEnoughBalanceError()
        await self._users_balance.remove_balance(
            BalanceChangeReason.buy_symbol, user_id, price * amount
        )
        await self._symbols.insert_or_add(user_id, symbol, amount)
        return price * amount


@dataclass
class MySymbolDTO:
    code: str
    amount: int
    price: SymbolPrice


class GetMySymbols:
    def __init__(
        self, symbols: SymbolsStorage, symbols_getter: SymbolsPriceGetter
    ) -> None:
        self._symbols = symbols
        self._symbols_getter = symbols_getter

    async def __call__(self, user_id: int) -> list[MySymbolDTO]:
        symbols = await self._symbols.get_all_user_symbols(user_id)
        return [
            MySymbolDTO(
                code=i.code,
                amount=i.amount,
                price=await self._symbols_getter.get_price(i.code),
            )
            for i in symbols
            if i.amount > 0
        ]


class SellSymbol:
    def __init__(
        self,
        symbols_getter: SymbolsPriceGetter,
        symbols: SymbolsStorage,
        users_balance: BalanceEditor,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols = symbols
        self._users_balance = users_balance

    async def __call__(self, user_id: int, symbol: str, amount: int) -> float:
        symbol = symbol.upper()
        user_amount = await self._symbols.get_amount(user_id, symbol)
        if user_amount < amount:
            raise NotEnoughSymbolsError()
        price = (await self._symbols_getter.get_price(symbol)).sell
        await self._users_balance.add_balance(
            BalanceChangeReason.sold_symbol, user_id, price * amount
        )
        await self._symbols.remove(user_id, symbol, amount)
        return price * amount


class FindTicker:
    def __init__(self, ticker_finder: TickerFinder) -> None:
        self._ticker_finder = ticker_finder

    async def __call__(self, name: str) -> list[SymbolTicker]:
        return await self._ticker_finder.find_ticker(name)
