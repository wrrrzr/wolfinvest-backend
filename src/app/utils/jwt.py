from typing import Any, Optional
from datetime import timedelta

import jwt
from passlib.context import CryptContext

from app.utils.funcs import get_current_time
from app.main.config import load_common_config

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)
AUTH_SECRET_KEY = load_common_config().auth_secret_key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_jwt_token(data: dict[str, Any]) -> str:
    data["exp"] = get_current_time() + EXPIRATION_TIME
    return jwt.encode(data, AUTH_SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(token, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
