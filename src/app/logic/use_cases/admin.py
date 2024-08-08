from app.logic.models import User, Role
from app.logic.exceptions import PermissionDenied
from app.logic.abstract import (
    UsersOneSelector,
    UsersAllSelector,
    UsersDeleter,
    UsersPasswordEditor,
)
from app.logic.abstract.transaction import Transaction
from app.logic.abstract.symbols_storage import SymbolsUsersDeletor
from app.logic.abstract.auth_manager import PasswordManager
from app.logic.abstract.refills_storage import RefillsUsersDeletor
from app.logic.abstract.currency_storage import CurrencyUsersDeletor


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
        refills: RefillsUsersDeletor,
        symbols: SymbolsUsersDeletor,
        currencies: CurrencyUsersDeletor,
        transaction: Transaction,
    ) -> None:
        self._users_selector = users_selector
        self._users_deleter = users_deleter
        self._refills = refills
        self._symbols = symbols
        self._currencies = currencies
        self._transaction = transaction

    async def __call__(self, user_id: int, target: int) -> None:
        await check_permissions(self._users_selector, user_id)
        await self._symbols.delete_all_user_symbols(target)
        await self._refills.delete_all_user_refills(target)
        await self._currencies.delete_all_user_currencies(target)
        await self._users_deleter.delete_user(target)
        await self._transaction.commit()


class ChangeUserPassword:
    def __init__(
        self,
        users_selector: UsersOneSelector,
        users_password: UsersPasswordEditor,
        password_manager: PasswordManager,
        transaction: Transaction,
    ) -> None:
        self._users_selector = users_selector
        self._users_password = users_password
        self._password_manager = password_manager
        self._transaction = transaction

    async def __call__(
        self, user_id: int, target: int, new_password: str
    ) -> None:
        await check_permissions(self._users_selector, user_id)
        new_password_hash = await self._password_manager.hash_password(
            new_password
        )
        await self._users_password.change_password(target, new_password_hash)
        await self._transaction.commit()
