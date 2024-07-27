from app.logic.abstract.currency_getter import CurrencyPriceGetter
from app.logic.abstract.users_storage import UsersOneSelector
from app.logic.abstract.currency_storage import (
    CurrencyUserAllSelector,
    CurrencyAdder,
)
from app.logic.balance_editor import BalanceEditor
from app.logic.models.balance_history import BalanceChangeReason
from app.logic.exceptions import NotEnoughBalanceError


class GetUserCurrencies:
    def __init__(self, currency_storage: CurrencyUserAllSelector) -> None:
        self._currency_storage = currency_storage

    async def __call__(self, user_id: int) -> dict[str, float]:
        return await self._currency_storage.get_all_user_currencies(user_id)


class GetCurrencyPrice:
    def __init__(self, currency_price: CurrencyPriceGetter) -> None:
        self._currency_price = currency_price

    async def __call__(self, currency: str) -> float:
        return await self._currency_price.get_price(currency)


class BuyCurrency:
    def __init__(
        self,
        currency_adder: CurrencyAdder,
        currency_price: CurrencyPriceGetter,
        users: UsersOneSelector,
        users_balance: BalanceEditor,
    ) -> None:
        self._currency_adder = currency_adder
        self._currency_price = currency_price
        self._users = users
        self._users_balance = users_balance

    async def __call__(self, user_id: int, ticker: str, amount: float) -> None:
        ticker = ticker.upper()
        price = await self._currency_price.get_price(ticker)
        user = await self._users.select_one_by_id(user_id)

        if user.balance < price * amount:
            raise NotEnoughBalanceError()

        await self._users_balance.remove_balance(
            BalanceChangeReason.buy_currency, user_id, price * amount
        )
        await self._currency_adder.add(user_id, ticker, amount, price)
        return


class SellCurrency:
    pass
