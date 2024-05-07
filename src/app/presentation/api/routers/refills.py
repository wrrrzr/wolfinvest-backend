from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from app.logic.refills import TakeRefill, GetMyRefills, MyRefillDTO
from ..depends import get_user_id

router = APIRouter(prefix="/refills", tags=["refills"])


@router.post("/take-refill")
@inject
async def take_refill(
    use_case: FromDishka[TakeRefill],
    amount: int,
    user_id: int = Depends(get_user_id),
) -> str:
    await use_case(user_id, amount)
    return "ok"


@router.get("/get-my-refills")
@inject
async def get_my_refills(
    use_case: FromDishka[GetMyRefills], user_id: int = Depends(get_user_id)
) -> list[MyRefillDTO]:
    return await use_case(user_id)
