from dataclasses import dataclass

from app.utils.dataclasses import object_to_dataclass
from app.logic.abstract import UsersStorage


@dataclass
class UserGetMeDTO:
    id: int
    balance: float
    username: str
    role: int


class GetMe:
    def __init__(self, users: UsersStorage) -> None:
        self._users = users

    async def __call__(self, user_id: int) -> UserGetMeDTO:
        res = await self._users.select_one_by_id(user_id)
        return object_to_dataclass(res, UserGetMeDTO)
