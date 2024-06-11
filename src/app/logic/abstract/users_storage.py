from abc import ABC, abstractmethod

from app.logic.models import User


class UsersStorage(ABC):
    @abstractmethod
    async def insert(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_balance(self, user_id: int, balance: float) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_balance(self, user_id: int, balance: float) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_balance(self, user_id: int, balance: float) -> None:
        raise NotImplementedError

    @abstractmethod
    async def change_password(self, user_id: int, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_one_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def select_one_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def select_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_new_user_id(self) -> int:
        raise NotImplementedError
