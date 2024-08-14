from dataclasses import dataclass
from datetime import datetime

from app.logic.abstract.storages.users import UsersStorage
from app.logic.models import User


@dataclass
class UsersMemory:
    data: list[User]


class MemoryCacheUsersStorage(UsersStorage):
    def __init__(self, inner: UsersStorage, memory: UsersMemory) -> None:
        self._inner = inner
        self._memory = memory

    @staticmethod
    def create_memory() -> UsersMemory:
        return UsersMemory([])

    async def insert(
        self, username: str, password: str, register_at: datetime
    ) -> None:
        await self._inner.insert(username, password, register_at)
        self._memory.data = await self.select_all()

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

    async def select_all(self) -> list[User]:
        return await self._inner.select_all()

    async def exists_by_username(self, username: str) -> bool:
        return await self._inner.exists_by_username(username)

    async def delete_user(self, user_id: int) -> None:
        await self._inner.delete_user(user_id)

    async def _check_user_and_update(self, user_id: int) -> None:
        if user_id not in self._memory.data:
            self._memory.data.append(
                await self._inner.select_one_by_id(user_id)
            )
