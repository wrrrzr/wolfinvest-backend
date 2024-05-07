from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.utils.dataclasses import object_to_dataclass
from app.logic.abstract import RefillsStorage
from app.logic.models import Refill
from .models import RefillModel


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
        await self._session.commit()
        return

    async def get_all_user_refills(self, user_id: int) -> list[Refill]:
        stmt = select(RefillModel).where(RefillModel.user_id == user_id)
        res = await self._session.execute(stmt)
        return [object_to_dataclass(i, Refill) for i in res.scalars().all()]
