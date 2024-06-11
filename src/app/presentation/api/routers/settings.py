from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.logic.settings import ChangePassword
from app.logic.exceptions import IncorrectPasswordError
from ..di import UserId


class ChangePasswordInfo(BaseModel):
    old_password: str
    new_password: str


router = APIRouter(prefix="/settings", tags=["settings"])


@router.post("/change-password")
@inject
async def change_password(
    use_case: FromDishka[ChangePassword],
    info: ChangePasswordInfo,
    user_id: FromDishka[UserId],
) -> str:
    try:
        await use_case(user_id, info.old_password, info.new_password)
    except IncorrectPasswordError:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return "ok"
