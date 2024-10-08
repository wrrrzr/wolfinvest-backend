from abc import ABC, abstractmethod
from datetime import datetime

from app.logic.models import User


class UsersAdder(ABC):
    @abstractmethod
    async def insert(
        self, username: str, password: str, register_at: datetime
    ) -> None:
        raise NotImplementedError


class UsersPasswordEditor(ABC):
    @abstractmethod
    async def change_password(self, user_id: int, password: str) -> None:
        raise NotImplementedError


class UsersOneSelector(ABC):
    @abstractmethod
    async def select_one_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def select_one_by_username(self, username: str) -> User:
        raise NotImplementedError


class UsersAllSelector(ABC):
    @abstractmethod
    async def select_all(self) -> list[User]:
        raise NotImplementedError


class UsersChecker(ABC):
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        raise NotImplementedError


class UsersDeleter(ABC):
    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        raise NotImplementedError


class UsersStorage(
    UsersAdder,
    UsersPasswordEditor,
    UsersOneSelector,
    UsersAllSelector,
    UsersChecker,
    UsersDeleter,
    ABC,
):
    pass
