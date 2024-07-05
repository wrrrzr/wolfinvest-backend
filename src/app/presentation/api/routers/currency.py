from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.logic.use_cases.currency import GetCurrencyPrice

router = APIRouter(prefix="/currency", tags=["currency"])


@router.post("/get-price")
@inject
async def take_refill(
    use_case: FromDishka[GetCurrencyPrice], currency: str
) -> float:
    return await use_case(currency)
