from unittest.mock import AsyncMock
from datetime import datetime

import pytest

from app.logic.models import User, Role
from app.logic.exceptions import PermissionDenied
from app.logic.abstract.auth_manager import PasswordManager
from app.logic.use_cases.admin import (
    check_permissions,
    GetAllUsers,
    DeleteUser,
    ChangeUserPassword,
)


class MockPasswordManager(PasswordManager):
    async def hash_password(self, password: str) -> str:
        return "hashed_" + password

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return "hashed_" + password == password_hash


def create_mock_users_selector(
    need_user_id: int, need_role: Role
) -> AsyncMock:
    async def side_effect(user_id: int) -> User:
        if user_id != need_user_id:
            raise AssertionError()
        return User(
            id=need_user_id,
            username="abc",
            password="def",
            role=need_role,
            register_at=datetime.now(),
        )

    users_selector = AsyncMock()
    users_selector.select_one_by_id.side_effect = side_effect
    return users_selector


async def test_check_permissions_for_owner() -> None:
    USER_ID = 100
    users_selector = create_mock_users_selector(USER_ID, Role.OWNER)

    await check_permissions(users_selector, USER_ID)
    users_selector.select_one_by_id.assert_awaited_once()


async def test_check_permissions_for_user() -> None:
    USER_ID = 533
    users_selector = create_mock_users_selector(USER_ID, Role.USER)

    with pytest.raises(PermissionDenied):
        await check_permissions(users_selector, USER_ID)
    users_selector.select_one_by_id.assert_awaited_once()


async def test_get_all_users() -> None:
    USER_ID = 44
    RETURN_VALUE = [
        User(
            id=3,
            username="ttttt",
            password="ttttt",
            role=Role.USER,
            register_at=datetime.now(),
        )
    ]

    users_selector = create_mock_users_selector(USER_ID, Role.OWNER)
    users_all = AsyncMock()
    users_all.select_all.return_value = RETURN_VALUE

    use_case = GetAllUsers(users_selector, users_all)
    assert await use_case(USER_ID) == RETURN_VALUE
    users_all.select_all.assert_awaited_once()


async def test_get_all_users_for_user() -> None:
    USER_ID = 44
    users_selector = create_mock_users_selector(USER_ID, Role.USER)
    users_all = AsyncMock()
    users_all.select_all.return_value = []
    use_case = GetAllUsers(users_selector, users_all)

    with pytest.raises(PermissionDenied):
        await use_case(USER_ID)
    users_all.select_all.assert_not_awaited()


async def test_delete_user() -> None:
    USER_ID = 777
    TARGET_ID = 94
    users_selector = create_mock_users_selector(USER_ID, Role.OWNER)
    users_deleter = AsyncMock()
    refills = AsyncMock()
    symbols = AsyncMock()
    currencies = AsyncMock()
    transaction = AsyncMock()
    use_case = DeleteUser(
        users_selector,
        users_deleter,
        refills,
        symbols,
        currencies,
        transaction,
    )

    await use_case(USER_ID, TARGET_ID)
    refills.delete_all_user_refills.assert_awaited_once_with(TARGET_ID)
    symbols.delete_all_user_symbols.assert_awaited_once_with(TARGET_ID)
    currencies.delete_all_user_currencies.assert_awaited_once_with(TARGET_ID)
    users_deleter.delete_user.assert_awaited_once_with(TARGET_ID)
    transaction.commit.assert_awaited_once()


async def test_delete_user_for_user() -> None:
    USER_ID = 777
    TARGET = 33
    users_selector = create_mock_users_selector(USER_ID, Role.USER)
    mock = AsyncMock()
    use_case = DeleteUser(users_selector, mock, mock, mock, mock, mock)

    with pytest.raises(PermissionDenied):
        await use_case(USER_ID, TARGET)
    mock.commit.assert_not_awaited()


async def test_change_user_password() -> None:
    USER_ID = 777
    TARGET = 33
    PASSWORD = "newpassword"
    users_selector = create_mock_users_selector(USER_ID, Role.OWNER)
    password_editor = AsyncMock()
    password_manager = MockPasswordManager()
    transaction = AsyncMock()
    use_case = ChangeUserPassword(
        users_selector, password_editor, password_manager, transaction
    )

    await use_case(USER_ID, TARGET, PASSWORD)
    password_editor.change_password.assert_awaited_once_with(
        TARGET, await password_manager.hash_password(PASSWORD)
    )
    transaction.commit.assert_awaited_once()


async def test_change_password_for_user() -> None:
    USER_ID = 181
    TARGET = 10
    users_selector = create_mock_users_selector(USER_ID, Role.USER)
    mock = AsyncMock()
    use_case = ChangeUserPassword(users_selector, mock, mock, mock)

    with pytest.raises(PermissionDenied):
        await use_case(USER_ID, TARGET, "newpswdb2")
    mock.commit.assert_not_awaited()
