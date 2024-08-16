from unittest.mock import AsyncMock
from datetime import datetime
from typing import Any

import pytest

from app.logic.use_cases.auth import RegisterUser, AuthUser
from app.logic.exceptions import (
    UsernameAlreadyTakenError,
    IncorrectUsernameError,
    IncorrectPasswordError,
)
from app.logic.models.user import User, Role
from app.logic.abstract.auth_manager import PasswordManager


class MockPasswordManager(PasswordManager):
    async def hash_password(self, password: str) -> str:
        return "hashed_" + password

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return "hashed_" + password == password_hash


async def test_register_user() -> None:
    CLOCKTIME = datetime.now()
    USERNAME = "newusername"
    PASSWORD = "1234"
    users_checker = AsyncMock()
    users_checker.exists_by_username.return_value = False
    users_adder = AsyncMock()
    password_manager = MockPasswordManager()
    transaction = AsyncMock()
    clock = AsyncMock()
    clock.get_current_time.return_value = CLOCKTIME
    use_case = RegisterUser(
        users_checker, users_adder, password_manager, transaction, clock
    )

    await use_case(USERNAME, PASSWORD)
    users_adder.insert.assert_awaited_once_with(
        USERNAME, await password_manager.hash_password(PASSWORD), CLOCKTIME
    )
    transaction.commit.assert_awaited_once()


async def test_register_user_with_taken_username() -> None:
    MOCKUSERNAME = "abcdef"
    PASSWORD = "0"
    users_checker = AsyncMock()
    users_checker.exists_by_username.side_effect = (
        lambda username: username == MOCKUSERNAME
    )
    users_adder = AsyncMock()
    password_manager = AsyncMock()
    transaction = AsyncMock()
    clock = AsyncMock()

    use_case = RegisterUser(
        users_checker, users_adder, password_manager, transaction, clock
    )

    with pytest.raises(UsernameAlreadyTakenError):
        await use_case(MOCKUSERNAME, PASSWORD)

    users_adder.insert.assert_not_awaited()
    transaction.commit.assert_not_awaited()


async def test_auth_user() -> None:
    TOKEN = "bhbhubherbrebheeknjc"
    USERNAME = "usrname"
    PASSWORD = "passwd"
    USER_ID = 150
    password_manager = MockPasswordManager()
    users_checker = AsyncMock()
    users_checker.exists_by_username.side_effect = (
        lambda username: username == USERNAME
    )
    users_selector = AsyncMock()
    users_selector.select_one_by_username.return_value = User(
        USER_ID,
        USERNAME,
        await password_manager.hash_password(PASSWORD),
        Role.USER,
        datetime.now(),
    )

    async def token_manager_side_effect(data: dict[str, Any]) -> str:
        if data["id"] != USER_ID:
            raise AssertionError
        return TOKEN

    token_manager = AsyncMock()
    token_manager.create_token.side_effect = token_manager_side_effect
    use_case = AuthUser(
        users_checker, users_selector, token_manager, password_manager
    )

    assert await use_case(USERNAME, PASSWORD) == TOKEN


async def test_auth_user_not_exists_username() -> None:
    users_checker = AsyncMock()
    users_checker.exists_by_username.return_value = False
    users_selector = AsyncMock()
    token_manager = AsyncMock()
    password_manager = AsyncMock()
    use_case = AuthUser(
        users_checker, users_selector, token_manager, password_manager
    )

    with pytest.raises(IncorrectUsernameError):
        await use_case("abcdef", "abcdef")


async def test_auth_user_incorrect_password() -> None:
    users_checker = AsyncMock()
    users_checker.exists_by_username.return_value = True
    users_selector = AsyncMock()
    users_selector.select_one_by_username.return_value = User(
        5,
        "aaaa",
        "pswd",
        Role.USER,
        datetime.now(),
    )
    token_manager = AsyncMock()
    password_manager = AsyncMock()
    password_manager.verify_password.return_value = False
    use_case = AuthUser(
        users_checker, users_selector, token_manager, password_manager
    )

    with pytest.raises(IncorrectPasswordError):
        await use_case("aaaa", "abcdef")
