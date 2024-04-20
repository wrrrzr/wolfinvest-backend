from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel

from app.logic.auth import RegisterUser, AuthUser
from app.logic.exceptions import (
    UsernameAlreadyTakenError,
    IncorrectUsernameError,
    IncorrectPasswordError,
)


class UserAuthInfo(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/reg")
@inject
async def reg(info: UserAuthInfo, use_case: FromDishka[RegisterUser]) -> str:
    try:
        await use_case(info.username, info.password)
    except UsernameAlreadyTakenError:
        raise HTTPException(
            status_code=401, detail="This username already taken"
        )
    return "ok"


@router.post("/auth")
@inject
async def auth(
    response: Response, info: UserAuthInfo, use_case: FromDishka[AuthUser]
) -> str:
    try:
        token = await use_case(info.username, info.password)
    except (IncorrectUsernameError, IncorrectPasswordError):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )
    response.set_cookie("token", token)
    return "ok"
