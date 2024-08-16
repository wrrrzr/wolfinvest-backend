from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from app.logic.abstract.storages.refills import RefillsStorage
from app.logic.dataclasses import objects_to_dataclasses
from app.logic.models import Refill
from app.adapters.sqlalchemy.models import RefillModel


class SQLAlchemyRefillsStorage(RefillsStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(
        self, user_id: int, amount: int, created_at: datetime
    ) -> None:
        stmt = insert(RefillModel).values(
            user_id=user_id, amount=amount, created_at=created_at
        )
        await self._session.execute(stmt)
        return

    async def get_all_user_refills(self, user_id: int) -> list[Refill]:
        stmt = select(RefillModel).where(RefillModel.user_id == user_id)
        res = await self._session.execute(stmt)
        return objects_to_dataclasses(res.scalars().all(), Refill)

    async def delete_all_user_refills(self, user_id: int) -> None:
        stmt = delete(RefillModel).where(RefillModel.user_id == user_id)
        await self._session.execute(stmt)
        return
