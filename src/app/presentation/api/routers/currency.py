from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException

from app.logic.use_cases.currency import (
    GetCurrencyPrice,
    BuyCurrency,
    GetUserCurrencies,
    SellCurrency,
    GetCurrenciesHistory,
)
from app.logic.models.currency import MyCurrencyDTO, CurrencyChange
from app.logic.exceptions import (
    NotEnoughBalanceError,
    NotEnoughCurrencyError,
    UnfoundCurrencyError,
)
from ..di import UserId

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/get-price")
@inject
async def get_price(
    use_case: FromDishka[GetCurrencyPrice], currency: str
) -> float:
    try:
        return await use_case(currency)
    except UnfoundCurrencyError:
        raise HTTPException(
            status_code=404, detail=f"Cannot find currency {currency}"
        )


@router.get("/get-my-currencies")
@inject
async def get_my_currencies(
    use_case: FromDishka[GetUserCurrencies], user_id: FromDishka[UserId]
) -> list[MyCurrencyDTO]:
    return await use_case(user_id)


@router.post("/buy-currency")
@inject
async def buy_currency(
    use_case: FromDishka[BuyCurrency],
    user_id: FromDishka[UserId],
    currency: str,
    amount: float,
) -> None:
    try:
        await use_case(user_id, currency, amount)
    except NotEnoughBalanceError:
        raise HTTPException(status_code=400, detail="not enough balance")
    except UnfoundCurrencyError:
        raise HTTPException(
            status_code=404, detail=f"Cannot find currency {currency}"
        )


@router.post("/sell-currency")
@inject
async def sell_currency(
    use_case: FromDishka[SellCurrency],
    user_id: FromDishka[UserId],
    currency: str,
    amount: float,
) -> None:
    try:
        await use_case(user_id, currency, amount)
    except NotEnoughCurrencyError:
        raise HTTPException(status_code=400, detail="not enough currency")
    except UnfoundCurrencyError:
        raise HTTPException(
            status_code=404, detail=f"Cannot find currency {currency}"
        )


@router.get("/get-currencies-history")
@inject
async def get_currencies_history(
    use_case: FromDishka[GetCurrenciesHistory], user_id: FromDishka[UserId]
) -> list[CurrencyChange]:
    return await use_case(user_id)
