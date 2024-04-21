from app.logic.abstract import UsersStorage
from app.logic.models import User

_memory: dict[int, User] = {}
_memory_usernames: dict[str, User] = {}
_memory_ids: dict[int, User] = {}
_memory_exists_usernames: dict[str, bool] = {}


class UsersCacheStorage(UsersStorage):
    def __init__(self, inner: UsersStorage) -> None:
        self._inner = inner

    async def insert(self, user: User) -> None:
        if user.id in _memory:
            return
        _memory[user.id] = user
        _memory_exists_usernames[user.username] = True
        await self._inner.insert(user)

    async def select_one_by_id(self, user_id: int) -> User:
        if user_id not in _memory_ids:
            _memory_ids[user_id] = await self._inner.select_one_by_id(user_id)
        return _memory_ids[user_id]

    async def select_one_by_username(self, username: str) -> User:
        if username not in _memory_usernames:
            _memory_usernames[username] = (
                await self._inner.select_one_by_username(username)
            )
        return _memory_usernames[username]

    async def exists_by_username(self, username: str) -> bool:
        if username not in _memory_exists_usernames:
            _memory_exists_usernames[username] = (
                await self._inner.exists_by_username(username)
            )
        return _memory_exists_usernames[username]

    async def get_new_user_id(self) -> int:
        return await self._inner.get_new_user_id()
