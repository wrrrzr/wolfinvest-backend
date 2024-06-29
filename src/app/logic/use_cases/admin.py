from app.logic.models import User, Role, BalanceChangeReason
from app.logic.exceptions import PermissionDenied
from app.logic.abstract import (
    UsersOneSelector,
    UsersAllSelector,
    UsersDeleter,
    UsersPasswordEditor,
    RefillsStorage,
    SymbolsStorage,
    AuthManager,
)
from app.logic.balance_editor import BalanceEditor


async def check_permissions(users: UsersOneSelector, user_id: int) -> None:
    user = await users.select_one_by_id(user_id)
    if user.role != Role.OWNER:
        raise PermissionDenied()


class GetAllUsers:
    def __init__(
        self, users_one: UsersOneSelector, users_all: UsersAllSelector
    ) -> None:
        self._users_one = users_one
        self._users_all = users_all

    async def __call__(self, user_id: int) -> list[User]:
        await check_permissions(self._users_one, user_id)
        return await self._users_all.select_all()


class DeleteUser:
    def __init__(
        self,
        users_selector: UsersOneSelector,
        users_deleter: UsersDeleter,
        refills: RefillsStorage,
        symbols: SymbolsStorage,
    ) -> None:
        self._users_selector = users_selector
        self._users_deleter = users_deleter
        self._refills = refills
        self._symbols = symbols

    async def __call__(self, user_id: int, target: int) -> None:
        await check_permissions(self._users_selector, user_id)
        await self._symbols.delete_all_user_symbols(target)
        await self._refills.delete_all_user_refills(target)
        await self._users_deleter.delete_user(target)


class ChangeUserPassword:
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
        self, user_id: int, target: int, new_password: str
    ) -> None:
        await check_permissions(self._users_selector, user_id)
        new_password_hash = await self._auth_manager.hash_password(
            new_password
        )
        await self._users_password.change_password(target, new_password_hash)


class SetUserBalance:
    def __init__(
        self, users: UsersOneSelector, users_balance: BalanceEditor
    ) -> None:
        self._users = users
        self._users_balance = users_balance

    async def __call__(
        self, user_id: int, target: int, new_balance: float
    ) -> None:
        await check_permissions(self._users, user_id)
        await self._users_balance.set_balance(
            BalanceChangeReason.admin_set, target, new_balance
        )
