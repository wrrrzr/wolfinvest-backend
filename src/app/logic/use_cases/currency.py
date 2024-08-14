from app.logic.abstract.currency_getter import CurrencyPriceGetter
from app.logic.abstract.storages.currency import (
    CurrencyUserAllSelector,
    CurrencyAdder,
    CurrencyRemover,
    CurrencyAmountSelector,
    CurrencyChangesSelector,
    MAIN_CURRENCY,
)
from app.logic.abstract.transaction import Transaction
from app.logic.models.currency import MyCurrencyDTO, Reason, CurrencyChange
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
        transaction: Transaction,
    ) -> None:
        self._currency_adder = currency_adder
        self._currency_remover = currency_remover
        self._currency_price = currency_price
        self._currency_amount = currency_amount
        self._transaction = transaction

    async def __call__(self, user_id: int, ticker: str, amount: float) -> None:
        ticker = ticker.upper()

        if ticker == MAIN_CURRENCY:
            return

        price = await self._currency_price.get_price(ticker)
        user_balance = await self._currency_amount.get_amount(
            user_id, MAIN_CURRENCY
        )

        if user_balance < price * amount:
            raise NotEnoughBalanceError()

        await self._currency_remover.remove(
            user_id,
            MAIN_CURRENCY,
            price * amount,
            price,
            Reason.sell,
        )
        await self._currency_adder.add(
            user_id, ticker, amount, price, Reason.buy
        )
        await self._transaction.commit()


class SellCurrency:
    def __init__(
        self,
        currency_remover: CurrencyRemover,
        currency_adder: CurrencyAdder,
        currency_price: CurrencyPriceGetter,
        currency_amount: CurrencyAmountSelector,
        transaction: Transaction,
    ) -> None:
        self._currency_remover = currency_remover
        self._currency_adder = currency_adder
        self._currency_price = currency_price
        self._currency_amount = currency_amount
        self._transaction = transaction

    async def __call__(self, user_id: int, ticker: str, amount: float) -> None:
        ticker = ticker.upper()

        if ticker == MAIN_CURRENCY:
            return

        price = await self._currency_price.get_price(ticker)
        user_amount = await self._currency_amount.get_amount(user_id, ticker)

        if user_amount < amount:
            raise NotEnoughCurrencyError()

        await self._currency_adder.add(
            user_id,
            MAIN_CURRENCY,
            price * amount,
            price,
            Reason.buy,
        )
        await self._currency_remover.remove(
            user_id, ticker, amount, price, Reason.sell
        )
        await self._transaction.commit()


class GetCurrenciesHistory:
    def __init__(self, currency_changes: CurrencyChangesSelector) -> None:
        self._currency_changes = currency_changes

    async def __call__(self, user_id: int) -> list[CurrencyChange]:
        return await self._currency_changes.get_all_user_currency_changes(
            user_id
        )
