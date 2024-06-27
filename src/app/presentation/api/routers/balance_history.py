from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.logic.use_cases.balance_history import GetMyBalanceHistory
from app.logic.models import BalanceChange
from ..di import UserId

router = APIRouter(prefix="/balance_history", tags=["balance_history"])


@router.get("/get-my-balance-history")
@inject
async def get_my_balance_history(
    use_case: FromDishka[GetMyBalanceHistory],
    user_id: FromDishka[UserId],
) -> list[BalanceChange]:
    return await use_case(user_id)
