from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.logic.models import User
from app.logic.admin import (
    GetAllUsers,
    DeleteUser,
    ChangeUserPassword,
    SetUserBalance,
)
from app.logic.exceptions import PermissionDenied
from ..di import UserId


class ChangeUserPasswordInfo(BaseModel):
    target: int
    new_password: str


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/get-all-users")
@inject
async def get_all_users(
    use_case: FromDishka[GetAllUsers],
    user_id: FromDishka[UserId],
) -> list[User]:
    try:
        return await use_case(user_id)
    except PermissionDenied:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/delete-user")
@inject
async def delete_user(
    use_case: FromDishka[DeleteUser],
    user_id: FromDishka[UserId],
    target: int,
) -> str:
    try:
        await use_case(user_id, target)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    return "ok"


@router.post("/change-user-password")
@inject
async def change_user_password(
    use_case: FromDishka[ChangeUserPassword],
    user_id: FromDishka[UserId],
    info: ChangeUserPasswordInfo,
) -> str:
    try:
        await use_case(user_id, info.target, info.new_password)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    return "ok"


@router.post("/set-user-balance")
@inject
async def set_user_balance(
    use_case: FromDishka[SetUserBalance],
    user_id: FromDishka[UserId],
    target: int,
    new_balance: float,
) -> str:
    try:
        await use_case(user_id, target, new_balance)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    return "ok"
