from dataclasses import dataclass

from .abstract import SymbolsGetter, UsersStorage, SymbolsStorage
from .exceptions import NotEnoughBalanceError, NotEnoughSymbolsError


class GetSymbol:
    def __init__(self, symbols_getter: SymbolsGetter) -> None:
        self._symbols_getter = symbols_getter

    async def __call__(self, symbol: str) -> float:
        return await self._symbols_getter.get_price(symbol)


class BuySymbol:
    def __init__(
        self,
        symbols_getter: SymbolsGetter,
        symbols: SymbolsStorage,
        users: UsersStorage,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols = symbols
        self._users = users

    async def __call__(self, user_id: int, symbol: str, amount: int) -> None:
        price = await self._symbols_getter.get_price(symbol)
        user = await self._users.select_one_by_id(user_id)
        if user.balance < price * amount:
            raise NotEnoughBalanceError()
        await self._users.remove_balance(user_id, price * amount)
        await self._symbols.insert_or_add(user_id, symbol, amount)


@dataclass
class MySymbolDTO:
    code: str
    amount: int
    price: float


class GetMySymbols:
    def __init__(
        self, symbols: SymbolsStorage, symbols_getter: SymbolsGetter
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
        symbols_getter: SymbolsGetter,
        symbols: SymbolsStorage,
        users: UsersStorage,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols = symbols
        self._users = users

    async def __call__(self, user_id: int, symbol: str, amount: int) -> float:
        user_amount = await self._symbols.get_amount(user_id, symbol)
        if user_amount < amount:
            raise NotEnoughSymbolsError()
        price = await self._symbols_getter.get_price(symbol)
        await self._users.add_balance(user_id, price * amount)
        await self._symbols.remove(user_id, symbol, amount)
        return price * amount
