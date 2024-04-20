from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from app.logic.users import GetMe, UserGetMeDTO
from ..depends import get_user_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
@inject
async def me(
    use_case: FromDishka[GetMe],
    user_id: int = Depends(get_user_id),
) -> UserGetMeDTO:
    return await use_case(user_id)
