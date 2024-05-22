from typing import NewType

from fastapi import HTTPException, Request
from dishka import Scope, Provider, from_context, provide

from app.logic.abstract import AuthManager

UserId = NewType("UserId", int)


class AuthProvider(Provider):
    scope = Scope.APP
    request = from_context(provides=Request)

    @provide(scope=Scope.REQUEST)
    async def get_user_id(
        self, auth_manager: AuthManager, request: Request
    ) -> UserId:
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(status_code=401, detail="You don't have token")

        data = await auth_manager.verify_token(token)

        if data is None:
            raise HTTPException(status_code=401, detail="Unknown token")

        return UserId(data["id"])
