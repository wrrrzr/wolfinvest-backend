from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Depends

from app.logic.symbols import GetSymbol, BuySymbol
from app.logic.exceptions import UnfoundSymbolError, NotEnoughBalanceError
from ..depends import get_user_id

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


@router.post("/buy-symbol")
@inject
async def buy_symbol(
    use_case: FromDishka[BuySymbol],
    symbol: str,
    amount: int,
    user_id: int = Depends(get_user_id),
) -> str:
    try:
        await use_case(user_id, symbol, amount)
        return "ok"
    except NotEnoughBalanceError:
        raise HTTPException(status_code=400, detail="not enough balance")
