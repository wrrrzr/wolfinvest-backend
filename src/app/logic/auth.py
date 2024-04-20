from app.utils.jwt import hash_password, verify_password, create_jwt_token
from .abstract import UsersStorage
from .models import User
from .exceptions import (
    UsernameAlreadyTakenError,
    IncorrectUsernameError,
    IncorrectPasswordError,
)


class RegisterUser:
    def __init__(self, users: UsersStorage) -> None:
        self._users = users

    async def __call__(self, username: str, password: str) -> None:
        if await self._users.exists_by_username(username):
            raise UsernameAlreadyTakenError()

        pass_hash = hash_password(password)
        new_id = await self._users.get_new_user_id()
        await self._users.insert(
            User(id=new_id, username=username, password=pass_hash)
        )


class AuthUser:
    def __init__(self, users: UsersStorage) -> None:
        self._users = users

    async def __call__(self, username: str, password: str) -> str:
        if not await self._users.exists_by_username(username):
            raise IncorrectUsernameError()

        user = await self._users.select_one_by_username(username)

        if not verify_password(password, user.password):
            raise IncorrectPasswordError()

        return create_jwt_token({"id": user.id})
