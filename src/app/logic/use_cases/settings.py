from app.logic.abstract import (
    UsersOneSelector,
    UsersPasswordEditor,
)
from app.logic.abstract.auth_manager import PasswordManager
from app.logic.exceptions import IncorrectPasswordError


class ChangePassword:
    def __init__(
        self,
        users_selector: UsersOneSelector,
        users_password: UsersPasswordEditor,
        password_manager: PasswordManager,
    ) -> None:
        self._users_selector = users_selector
        self._users_password = users_password
        self._password_manager = password_manager

    async def __call__(
        self, user_id: int, old_password: str, new_password: str
    ) -> None:
        user = await self._users_selector.select_one_by_id(user_id)

        if not await self._password_manager.verify_password(
            old_password, user.password
        ):
            raise IncorrectPasswordError()

        new_password_hash = await self._password_manager.hash_password(
            new_password
        )

        await self._users_password.change_password(user_id, new_password_hash)
