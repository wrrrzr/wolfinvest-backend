from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException

from app.logic.symbols import GetSymbol

router = APIRouter(prefix="/symbols", tags=["symbols"])


@router.get("/get-price")
@inject
async def get_price(symbol: str, use_case: FromDishka[GetSymbol]) -> float:
    res = await use_case(symbol)
    if res is None:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )
    return res
