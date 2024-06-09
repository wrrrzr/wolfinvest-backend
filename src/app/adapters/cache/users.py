from dataclasses import dataclass

from app.logic.abstract import UsersStorage
from app.logic.models import User


@dataclass
class UsersMemory:
    data: list[User]


def create_users_memory() -> UsersMemory:
    return UsersMemory([])


class UsersCacheStorage(UsersStorage):
    def __init__(self, inner: UsersStorage, memory: UsersMemory) -> None:
        self._inner = inner
        self._memory = memory

    async def insert(self, user: User) -> None:
        if user.id in self._memory.data:
            return
        self._memory.data.append(user)
        await self._inner.insert(user)

    async def add_balance(self, user_id: int, balance: float) -> None:
        await self._check_user_and_update(user_id)
        await self._inner.add_balance(user_id, balance)
        list(filter(lambda x: x.id == user_id, self._memory.data))[
            0
        ].balance += balance

    async def remove_balance(self, user_id: int, balance: float) -> None:
        await self._check_user_and_update(user_id)
        await self._inner.remove_balance(user_id, balance)
        list(filter(lambda x: x.id == user_id, self._memory.data))[
            0
        ].balance -= balance

    async def change_password(self, user_id: int, password: str) -> None:
        await self._check_user_and_update(user_id)
        await self._inner.change_password(user_id, password)
        list(filter(lambda x: x.id == user_id, self._memory.data))[
            0
        ].password = password

    async def select_one_by_id(self, user_id: int) -> User:
        await self._check_user_and_update(user_id)
        return list(filter(lambda x: x.id == user_id, self._memory.data))[0]

    async def select_one_by_username(self, username: str) -> User:
        if username not in self._memory.data:
            self._memory.data.append(
                await self._inner.select_one_by_username(username)
            )
        return list(
            filter(lambda x: x.username == username, self._memory.data)
        )[0]

    async def exists_by_username(self, username: str) -> bool:
        return await self._inner.exists_by_username(username)

    async def get_new_user_id(self) -> int:
        return await self._inner.get_new_user_id()

    async def _check_user_and_update(self, user_id: int) -> None:
        if user_id not in self._memory.data:
            self._memory.data.append(
                await self._inner.select_one_by_id(user_id)
            )
