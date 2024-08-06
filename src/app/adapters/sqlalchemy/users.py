from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete
from sqlalchemy.sql.expression import func

from app.utils.dataclasses import object_to_dataclass, objects_to_dataclasses
from app.logic.abstract import UsersStorage
from app.logic.models import User
from .models import UserModel

FIRST_ID = 1


class SQLAlchemyUsersStorage(UsersStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, user: User) -> None:
        stmt = insert(UserModel).values(
            id=user.id,
            username=user.username,
            password=user.password,
            register_at=user.register_at,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def change_password(self, user_id: int, password: str) -> None:
        stmt = (
            update(UserModel)
            .values(password=UserModel.password)
            .where(UserModel.id == user_id)
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def select_one_by_id(self, user_id: int) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        res = (await self._session.execute(stmt)).scalar_one()
        return object_to_dataclass(res, User)

    async def select_one_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.username == username)
        res = (await self._session.execute(stmt)).scalar_one()
        return object_to_dataclass(res, User)

    async def select_all(self) -> list[User]:
        stmt = select(UserModel)
        res = await self._session.execute(stmt)
        return objects_to_dataclasses(res.scalars().all(), User)

    async def exists_by_username(self, username: str) -> bool:
        stmt = exists(UserModel).where(UserModel.username == username).select()
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def get_new_user_id(self) -> int:
        stmt = select(func.max(UserModel.id))
        res = await self._session.execute(stmt)
        return (res.scalar_one_or_none() or FIRST_ID) + 1
