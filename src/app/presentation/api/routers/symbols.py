from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Depends

from app.logic.symbols import (
    GetSymbol,
    BuySymbol,
    GetMySymbols,
    SellSymbol,
    MySymbolDTO,
)
from app.logic.exceptions import (
    UnfoundSymbolError,
    NotEnoughBalanceError,
    NotEnoughSymbolsError,
)
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
    except UnfoundSymbolError:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )


@router.get("/get-my-symbols")
@inject
async def get_my_symbols(
    use_case: FromDishka[GetMySymbols], user_id: int = Depends(get_user_id)
) -> list[MySymbolDTO]:
    return await use_case(user_id)


@router.post("/sell-symbol")
@inject
async def sell_symbol(
    use_case: FromDishka[SellSymbol],
    symbol: str,
    amount: int,
    user_id: int = Depends(get_user_id),
) -> float:
    try:
        res = await use_case(user_id, symbol, amount)
    except NotEnoughSymbolsError:
        raise HTTPException(status_code=400, detail="not enough symbol")
    except UnfoundSymbolError:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )
    return res
