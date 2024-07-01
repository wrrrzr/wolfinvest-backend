from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException

from app.logic.use_cases.symbols import (
    GetSymbol,
    GetSymbolHistory,
    BuySymbol,
    GetMySymbols,
    SellSymbol,
    MySymbolDTO,
    FindTicker,
)
from app.logic.exceptions import (
    UnfoundSymbolError,
    NotEnoughBalanceError,
    NotEnoughSymbolsError,
)
from app.logic.models import (
    SymbolHistory,
    SymbolTicker,
    SymbolHistoryInterval,
    SymbolData,
)
from ..di import UserId

router = APIRouter(prefix="/symbols", tags=["symbols"])


@router.get("/get-symbol")
@inject
async def get_symbol(
    symbol: str, use_case: FromDishka[GetSymbol]
) -> SymbolData:
    try:
        return await use_case(symbol)
    except UnfoundSymbolError:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )


@router.get("/get-history")
@inject
async def get_history(
    interval: SymbolHistoryInterval,
    symbol: str,
    use_case: FromDishka[GetSymbolHistory],
) -> list[SymbolHistory]:
    try:
        return await use_case(interval, symbol)
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
    user_id: FromDishka[UserId],
) -> float:
    try:
        return await use_case(user_id, symbol, amount)
    except NotEnoughBalanceError:
        raise HTTPException(status_code=400, detail="not enough balance")
    except UnfoundSymbolError:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )


@router.get("/get-my-symbols")
@inject
async def get_my_symbols(
    use_case: FromDishka[GetMySymbols], user_id: FromDishka[UserId]
) -> list[MySymbolDTO]:
    return await use_case(user_id)


@router.post("/sell-symbol")
@inject
async def sell_symbol(
    use_case: FromDishka[SellSymbol],
    symbol: str,
    amount: int,
    user_id: FromDishka[UserId],
) -> float:
    try:
        return await use_case(user_id, symbol, amount)
    except NotEnoughSymbolsError:
        raise HTTPException(status_code=400, detail="not enough symbol")
    except UnfoundSymbolError:
        raise HTTPException(
            status_code=404, detail=f"Symbol named {symbol} not found"
        )


@router.get("/get-symbol-ticker")
@inject
async def get_symbol_ticker(
    name: str, use_case: FromDishka[FindTicker]
) -> list[SymbolTicker]:
    return await use_case(name)
