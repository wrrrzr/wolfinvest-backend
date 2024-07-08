from typing import Any
from datetime import timedelta

import jwt

from app.utils.funcs import get_current_time
from app.logic.abstract.auth_manager import TokenManager
from app.logic.models import JWTConfig
from app.logic.exceptions import VerifyTokenError

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(hours=6)


class JWTTokenManager(TokenManager):
    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    async def create_token(self, data: dict[str, Any]) -> str:
        data["exp"] = get_current_time() + EXPIRATION_TIME
        return jwt.encode(
            data, self._config.auth_secret_key, algorithm=ALGORITHM
        )

    async def verify_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                token, self._config.auth_secret_key, algorithms=[ALGORITHM]
            )
        except jwt.PyJWTError:
            raise VerifyTokenError()
