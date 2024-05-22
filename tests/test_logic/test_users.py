import pytest

from app.logic.abstract import UsersStorage
from app.logic.models import User
from app.logic.users import GetMe, UserGetMeDTO


class MockUsersStorage(UsersStorage):
    async def insert() -> None:
        pass

    async def select_one_by_username() -> None:
        pass

    async def exists_by_username() -> None:
        pass

    async def add_balance() -> None:
        pass

    async def remove_balance() -> None:
        pass

    async def get_new_user_id() -> None:
        pass

    async def select_one_by_id(self, user_id: int) -> User:
        return User(
            id=user_id,
            balance=0,
            username=f"user{user_id}",
            password=f"{user_id}password",
        )


@pytest.mark.parametrize("id", [5, 1, 5, 123456719])
async def test_get_me(id: int) -> None:
    use_case = GetMe(MockUsersStorage())
    res = await use_case(id)
    assert isinstance(res, UserGetMeDTO)
    assert res.id == id
    assert res.username == f"user{id}"
