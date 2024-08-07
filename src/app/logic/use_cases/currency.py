from app.logic.abstract.currency_getter import CurrencyPriceGetter
from app.logic.abstract.currency_storage import (
    CurrencyUserAllSelector,
    CurrencyAdder,
    CurrencyRemover,
    CurrencyAmountSelector,
    MAIN_CURRENCY,
)
from app.logic.models.currency import MyCurrencyDTO
from app.logic.exceptions import NotEnoughBalanceError, NotEnoughCurrencyError


class GetUserCurrencies:
    def __init__(self, currency_storage: CurrencyUserAllSelector) -> None:
        self._currency_storage = currency_storage

    async def __call__(self, user_id: int) -> list[MyCurrencyDTO]:
        currencies = await self._currency_storage.get_all_user_currencies(
            user_id
        )
        res = []

        for ticker, data in currencies.items():
            if data.amount <= 0:
                continue
            res.append(
                MyCurrencyDTO(
                    ticker=ticker,
                    amount=data.amount,
                )
            )
        return res


class GetCurrencyPrice:
    def __init__(self, currency_price: CurrencyPriceGetter) -> None:
        self._currency_price = currency_price

    async def __call__(self, currency: str) -> float:
        return await self._currency_price.get_price(currency)


class BuyCurrency:
    def __init__(
        self,
        currency_adder: CurrencyAdder,
        currency_remover: CurrencyRemover,
        currency_price: CurrencyPriceGetter,
        currency_amount: CurrencyAmountSelector,
    ) -> None:
        self._currency_adder = currency_adder
        self._currency_remover = currency_remover
        self._currency_price = currency_price
        self._currency_amount = currency_amount

    async def __call__(self, user_id: int, ticker: str, amount: float) -> None:
        ticker = ticker.upper()
        price = await self._currency_price.get_price(ticker)
        user_balance = await self._currency_amount.get_amount(
            user_id, MAIN_CURRENCY
        )

        if user_balance < price * amount:
            raise NotEnoughBalanceError()

        await self._currency_remover.remove(
            user_id, MAIN_CURRENCY, price * amount, price
        )
        await self._currency_adder.add(user_id, ticker, amount, price)
        return


class SellCurrency:
    def __init__(
        self,
        currency_remover: CurrencyRemover,
        currency_adder: CurrencyAdder,
        currency_price: CurrencyPriceGetter,
        currency_amount: CurrencyAmountSelector,
    ) -> None:
        self._currency_remover = currency_remover
        self._currency_adder = currency_adder
        self._currency_price = currency_price
        self._currency_amount = currency_amount

    async def __call__(self, user_id: int, ticker: str, amount: float) -> None:
        ticker = ticker.upper()
        price = await self._currency_price.get_price(ticker)
        user_amount = await self._currency_amount.get_amount(user_id, ticker)

        if user_amount < amount:
            raise NotEnoughCurrencyError()

        await self._currency_adder.add(
            user_id, MAIN_CURRENCY, price * amount, price
        )
        await self._currency_remover.remove(user_id, ticker, amount, price)
        return
