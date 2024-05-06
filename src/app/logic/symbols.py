from .abstract import SymbolsGetter, UsersStorage, SymbolsStorage
from .exceptions import NotEnoughBalanceError


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
