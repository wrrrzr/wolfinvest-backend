from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException

from app.logic.symbols import GetSymbol
from app.logic.exceptions import UnfoundSymbolError

router = APIRouter(prefix="/symbols", tags=["symbols"])


@router.get("/get-price")
@inject
async def get_price(symbol: str, use_case: FromDishka[GetSymbol]) -> float:
    try:
        return await use_case(symbol)
    except UnfoundSymbolError:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )
