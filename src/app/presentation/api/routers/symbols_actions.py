from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.logic.use_cases.symbols_actions import (
    GetMySymbolsActions,
    MySymbolActionDTO,
)
from ..di import UserId


router = APIRouter(prefix="/symbols_actions", tags=["symbols_actions"])


@router.get("/get-my-symbols-actions")
@inject
async def get_my_symbols_actions(
    user_id: FromDishka[UserId],
    symbol: str,
    use_case: FromDishka[GetMySymbolsActions],
) -> list[MySymbolActionDTO]:
    return await use_case(user_id, symbol)
