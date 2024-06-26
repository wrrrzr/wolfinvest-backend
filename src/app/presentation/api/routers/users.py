from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.logic.use_cases.users import GetMe, UserGetMeDTO
from ..di import UserId

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
@inject
async def me(
    use_case: FromDishka[GetMe],
    user_id: FromDishka[UserId],
) -> UserGetMeDTO:
    return await use_case(user_id)
