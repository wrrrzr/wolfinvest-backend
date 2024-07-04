from typing import Any, Optional
from datetime import timedelta

import jwt
from passlib.context import CryptContext

from app.utils.funcs import get_current_time
from app.logic.abstract import AuthManager
from app.logic.models import JWTConfig

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(hours=6)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTAuthManager(AuthManager):
    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    async def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    async def create_token(self, data: dict[str, Any]) -> str:
        auth_secret_key = self._config.auth_secret_key
        data["exp"] = get_current_time() + EXPIRATION_TIME
        return jwt.encode(data, auth_secret_key, algorithm=ALGORITHM)

    async def verify_token(self, token: str) -> Optional[dict[str, Any]]:
        auth_secret_key = self._config.auth_secret_key
        try:
            return jwt.decode(token, auth_secret_key, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return None
