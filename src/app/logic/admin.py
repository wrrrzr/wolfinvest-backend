from app.logic.models import User, Role
from .exceptions import PermissionDenied
from .abstract import UsersStorage, RefillsStorage, SymbolsStorage, AuthManager


async def check_permissions(users: UsersStorage, user_id: int) -> None:
    user = await users.select_one_by_id(user_id)
    if user.role != Role.OWNER:
        raise PermissionDenied()


class GetAllUsers:
    def __init__(self, users: UsersStorage) -> None:
        self._users = users

    async def __call__(self, user_id: int) -> list[User]:
        await check_permissions(self._users, user_id)
        return await self._users.select_all()


class DeleteUser:
    def __init__(
        self,
        users: UsersStorage,
        refills: RefillsStorage,
        symbols: SymbolsStorage,
    ) -> None:
        self._users = users
        self._refills = refills
        self._symbols = symbols

    async def __call__(self, user_id: int, target: int) -> None:
        await check_permissions(self._users, user_id)
        await self._symbols.delete_all_user_symbols(target)
        await self._refills.delete_all_user_refills(target)
        await self._users.delete_user(target)


class ChangeUserPassword:
    def __init__(self, users: UsersStorage, auth_manager: AuthManager) -> None:
        self._users = users
        self._auth_manager = auth_manager

    async def __call__(
        self, user_id: int, target: int, new_password: str
    ) -> None:
        await check_permissions(self._users, user_id)
        new_password_hash = await self._auth_manager.hash_password(
            new_password
        )
        await self._users.change_password(target, new_password_hash)


class SetUserBalance:
    def __init__(self, users: UsersStorage) -> None:
        self._users = users

    async def __call__(
        self, user_id: int, target: int, new_balance: float
    ) -> None:
        await check_permissions(self._users, user_id)
        await self._users.set_balance(target, new_balance)
