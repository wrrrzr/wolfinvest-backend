from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists
from sqlalchemy.sql.expression import func

from app.logic.abstract import UsersStorage
from app.logic.models import User
from .models import UserModel

FIRST_ID = 1


class SQLAlchemyUsersStorage(UsersStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, user: User) -> None:
        stmt = insert(UserModel).values(
            id=user.id, username=user.username, password=user.password
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def add_balance(self, user_id: int, balance: int) -> None:
        stmt = update(UserModel).values(balance=UserModel.balance + balance)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def remove_balance(self, user_id: int, balance: int) -> None:
        stmt = update(UserModel).values(balance=UserModel.balance - balance)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def select_one_by_id(self, user_id: int) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        res = await self._session.execute(stmt)
        res = res.scalar_one()
        return User(
            id=res.id,
            balance=res.balance,
            username=res.username,
            password=res.password,
        )

    async def select_one_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.username == username)
        res = await self._session.execute(stmt)
        res = res.scalar_one()
        return User(
            id=res.id,
            balance=res.balance,
            username=res.username,
            password=res.password,
        )

    async def exists_by_username(self, username: str) -> bool:
        stmt = exists(UserModel).where(UserModel.username == username).select()
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_new_user_id(self) -> int:
        stmt = select(func.max(UserModel.id))
        res = await self._session.execute(stmt)
        return (res.scalar_one_or_none() or FIRST_ID) + 1
