from unittest.mock import AsyncMock
from datetime import datetime

import pytest

from app.logic.models import User, Role
from app.logic.exceptions import PermissionDenied
from app.logic.use_cases.admin import check_permissions


async def test_check_permissions_for_owner() -> None:
    USER_ID = 100

    async def side_effect(user_id: int) -> User:
        if user_id != USER_ID:
            raise AssertionError()
        return User(
            id=USER_ID,
            username="abc",
            password="def",
            role=Role.OWNER,
            register_at=datetime.now(),
        )

    users_selector = AsyncMock()
    users_selector.select_one_by_id.side_effect = side_effect

    await check_permissions(users_selector, USER_ID)
    users_selector.select_one_by_id.assert_awaited_once()


async def test_check_permissions_for_user() -> None:
    USER_ID = 553

    async def side_effect(user_id: int) -> User:
        if user_id != USER_ID:
            raise AssertionError()
        return User(
            id=USER_ID,
            username="usr",
            password="1234",
            role=Role.USER,
            register_at=datetime.now(),
        )

    users_selector = AsyncMock()
    users_selector.select_one_by_id.side_effect = side_effect

    with pytest.raises(PermissionDenied):
        await check_permissions(users_selector, USER_ID)
    users_selector.select_one_by_id.assert_awaited_once()
