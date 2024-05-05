from dataclasses import dataclass

from .abstract import UsersStorage


@dataclass
class UserGetMeDTO:
    id: int
    balance: int
    username: str


class GetMe:
    def __init__(self, users: UsersStorage) -> None:
        self._users = users

    async def __call__(self, user_id: int) -> UserGetMeDTO:
        res = await self._users.select_one_by_id(user_id)
        return UserGetMeDTO(
            id=res.id, balance=res.balance, username=res.username
        )
