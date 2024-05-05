from .abstract import SymbolsGetter, UsersStorage


class GetSymbol:
    def __init__(self, symbols_getter: SymbolsGetter) -> None:
        self._symbols_getter = symbols_getter

    async def __call__(self, symbol: str) -> float:
        return await self._symbols_getter.get_price(symbol)


class BuySymbol:
    def __init__(
        self,
        symbols_getter: SymbolsGetter,
        symbols: None,
        users: UsersStorage,
    ) -> None:
        self._symbols_getter = symbols_getter
        self._symbols = symbols
        self._users = users

    async def __call__(self, user_id: int, symbol: str, amount: int) -> None:
        price = self._symbols_getter.get_price(symbol)
        if price is None:
            pass
