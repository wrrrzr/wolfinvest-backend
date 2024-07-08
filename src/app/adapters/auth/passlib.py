from passlib.context import CryptContext

from app.logic.abstract.auth_manager import PasswordManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasslibPasswordManager(PasswordManager):
    async def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)
