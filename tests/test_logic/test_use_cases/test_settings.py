from unittest.mock import AsyncMock

import pytest

from app.logic.use_cases.settings import ChangePassword
from app.logic.abstract.storages.users import UsersOneSelector
from app.logic.abstract.auth_manager import PasswordManager
from app.logic.exceptions import IncorrectPasswordError
from app.logic.models.user import User, USER_DEFAULT_ROLE
from app.utils.funcs import get_current_time


class MockUsersStorage(UsersOneSelector):
    async def select_one_by_username() -> None:
        pass

    async def select_one_by_id(self, user_id: int) -> User:
        return User(
            id=user_id,
            username=f"user{user_id}",
            password=f"hashed_{user_id}password",
            role=USER_DEFAULT_ROLE,
            register_at=get_current_time(),
        )


class MockPasswordManager(PasswordManager):
    async def hash_password(self, password: str) -> str:
        return "hashed_" + password

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return "hashed_" + password == password_hash


@pytest.fixture
def users_selector() -> MockUsersStorage:
    return MockUsersStorage()


@pytest.fixture
def password_manager() -> MockPasswordManager:
    return MockPasswordManager()


async def test_change_password(users_selector, password_manager) -> None:
    transaction = AsyncMock()
    password_editor = AsyncMock()
    use_case = ChangePassword(
        users_selector, password_editor, password_manager, transaction
    )

    await use_case(123, "123password", "npass")

    password_editor.change_password.assert_awaited_once()
    transaction.commit.assert_awaited_once()


async def test_incorrect_change_password(
    users_selector, password_manager
) -> None:
    transaction = AsyncMock()
    password_editor = AsyncMock()
    use_case = ChangePassword(
        users_selector, password_editor, password_manager, transaction
    )

    with pytest.raises(IncorrectPasswordError):
        await use_case(55, "incorrectpswd", "abcdef")

    password_editor.change_password.assert_not_awaited()
    transaction.commit.assert_not_awaited()
