import pytest

from app.logic.abstract import UsersOneSelector
from app.logic.models import User, Role
from app.logic.exceptions import PermissionDenied
from app.logic.use_cases.admin import check_permissions


class MockUsersOneSelector(UsersOneSelector):
    def __init__(self, data: list[User]) -> None:
        self.data = data

    async def select_one_by_id(self, user_id: int) -> User:
        return list(filter(lambda x: x.id == user_id, self.data))[0]

    async def select_one_by_username(self, username: str) -> User:
        return list(filter(lambda x: x.username == username, self.data))[0]


async def test_check_permissions_for_owner() -> None:
    user_id = 100
    await check_permissions(
        MockUsersOneSelector(
            [
                User(
                    id=user_id,
                    balance=1.5,
                    username="abc",
                    password="def",
                    role=Role.OWNER,
                )
            ]
        ),
        user_id,
    )


async def test_check_permissions_for_user() -> None:
    user_id = 100
    with pytest.raises(PermissionDenied):
        await check_permissions(
            MockUsersOneSelector(
                [
                    User(
                        id=user_id,
                        balance=0.3,
                        username="usr",
                        password="1234",
                        role=Role.USER,
                    )
                ]
            ),
            user_id,
        )
