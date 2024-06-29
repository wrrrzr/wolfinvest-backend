from app.logic.abstract import (
    UsersOneSelector,
    UsersPasswordEditor,
    AuthManager,
)
from app.logic.exceptions import IncorrectPasswordError


class ChangePassword:
    def __init__(
        self,
        users_selector: UsersOneSelector,
        users_password: UsersPasswordEditor,
        auth_manager: AuthManager,
    ) -> None:
        self._users_selector = users_selector
        self._users_password = users_password
        self._auth_manager = auth_manager

    async def __call__(
        self, user_id: int, old_password: str, new_password: str
    ) -> None:
        user = await self._users_selector.select_one_by_id(user_id)

        if not await self._auth_manager.verify_password(
            old_password, user.password
        ):
            raise IncorrectPasswordError()

        new_password_hash = await self._auth_manager.hash_password(
            new_password
        )

        await self._users_password.change_password(user_id, new_password_hash)
