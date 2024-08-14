from app.logic.abstract.storages.users import (
    UsersChecker,
    UsersAdder,
    UsersOneSelector,
)
from app.logic.abstract.auth_manager import TokenManager, PasswordManager
from app.logic.abstract.transaction import Transaction
from app.logic.exceptions import (
    UsernameAlreadyTakenError,
    IncorrectUsernameError,
    IncorrectPasswordError,
)
from app.utils.funcs import get_current_time


class RegisterUser:
    def __init__(
        self,
        users_checker: UsersChecker,
        users_adder: UsersAdder,
        password_manager: PasswordManager,
        transaction: Transaction,
    ) -> None:
        self._users_checker = users_checker
        self._users_adder = users_adder
        self._password_manager = password_manager
        self._transaction = transaction

    async def __call__(self, username: str, password: str) -> None:
        if await self._users_checker.exists_by_username(username):
            raise UsernameAlreadyTakenError()

        pass_hash = await self._password_manager.hash_password(password)
        await self._users_adder.insert(username, pass_hash, get_current_time())
        await self._transaction.commit()


class AuthUser:
    def __init__(
        self,
        users_checker: UsersChecker,
        users_selector: UsersOneSelector,
        token_manager: TokenManager,
        password_manager: PasswordManager,
    ) -> None:
        self._users_checker = users_checker
        self._users_selector = users_selector
        self._token_manager = token_manager
        self._password_manager = password_manager

    async def __call__(self, username: str, password: str) -> str:
        if not await self._users_checker.exists_by_username(username):
            raise IncorrectUsernameError()

        user = await self._users_selector.select_one_by_username(username)

        if not await self._password_manager.verify_password(
            password, user.password
        ):
            raise IncorrectPasswordError()

        return await self._token_manager.create_token({"id": user.id})
