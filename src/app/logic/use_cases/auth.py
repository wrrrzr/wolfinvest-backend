from app.logic.abstract import UsersStorage, AuthManager
from app.logic.models import User, USER_DEFAULT_ROLE
from app.logic.exceptions import (
    UsernameAlreadyTakenError,
    IncorrectUsernameError,
    IncorrectPasswordError,
)

DEFAULT_BALANCE = 0


class RegisterUser:
    def __init__(self, users: UsersStorage, auth_manager: AuthManager) -> None:
        self._users = users
        self._auth_manager = auth_manager

    async def __call__(self, username: str, password: str) -> None:
        if await self._users.exists_by_username(username):
            raise UsernameAlreadyTakenError()

        pass_hash = await self._auth_manager.hash_password(password)
        new_id = await self._users.get_new_user_id()
        await self._users.insert(
            User(
                id=new_id,
                balance=DEFAULT_BALANCE,
                username=username,
                password=pass_hash,
                role=USER_DEFAULT_ROLE,
            )
        )


class AuthUser:
    def __init__(self, users: UsersStorage, auth_manager: AuthManager) -> None:
        self._users = users
        self._auth_manager = auth_manager

    async def __call__(self, username: str, password: str) -> str:
        if not await self._users.exists_by_username(username):
            raise IncorrectUsernameError()

        user = await self._users.select_one_by_username(username)

        if not await self._auth_manager.verify_password(
            password, user.password
        ):
            raise IncorrectPasswordError()

        return await self._auth_manager.create_token({"id": user.id})
