from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException

from app.logic.use_cases.currency import (
    GetCurrencyPrice,
    BuyCurrency,
    GetUserCurrencies,
)
from app.logic.exceptions import NotEnoughBalanceError
from ..di import UserId

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/get-price")
@inject
async def get_price(
    use_case: FromDishka[GetCurrencyPrice], currency: str
) -> float:
    return await use_case(currency)


@router.get("/get-my-currencies")
@inject
async def get_my_currencies(
    use_case: FromDishka[GetUserCurrencies], user_id: FromDishka[UserId]
) -> dict[str, float]:
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
