from typing import Any, Optional
from datetime import timedelta

import jwt
from passlib.context import CryptContext

from app.utils.funcs import get_current_time
from app.config import load_jwt_config
from app.logic.abstract import AuthManager

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)
AUTH_SECRET_KEY = load_jwt_config().auth_secret_key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTAuthManager(AuthManager):
    async def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    async def create_token(self, data: dict[str, Any]) -> str:
        data["exp"] = get_current_time() + EXPIRATION_TIME
        return jwt.encode(data, AUTH_SECRET_KEY, algorithm=ALGORITHM)

    async def verify_token(self, token: str) -> Optional[dict[str, Any]]:
        try:
            return jwt.decode(token, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return None
