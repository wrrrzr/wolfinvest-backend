from typing import NewType

from fastapi import HTTPException, Request
from dishka import Scope, Provider, from_context, provide

from app.logic.abstract.auth_manager import TokenManager

UserId = NewType("UserId", int)


class AuthProvider(Provider):
    scope = Scope.APP
    request = from_context(provides=Request)

    @provide(scope=Scope.REQUEST)
    async def get_user_id(
        self, token_manager: TokenManager, request: Request
    ) -> UserId:
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(status_code=401, detail="You don't have token")

        data = await token_manager.verify_token(token)

        if data is None:
            raise HTTPException(status_code=401, detail="Unknown token")

        return UserId(data["id"])
