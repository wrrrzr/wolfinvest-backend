from abc import ABC, abstractmethod
from typing import Any, Optional


class PasswordManager(ABC):
    @abstractmethod
    async def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_password(self, password: str, password_hash: str) -> bool:
        raise NotImplementedError


class TokenManager(ABC):
    @abstractmethod
    async def create_token(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_token(self, token: str) -> Optional[dict[str, Any]]:
        raise NotImplementedError


class AuthManager(PasswordManager, TokenManager, ABC):
    pass
