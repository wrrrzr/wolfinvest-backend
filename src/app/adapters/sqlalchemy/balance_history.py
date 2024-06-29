from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.logic.abstract import BalanceHistoryEditor, BalanceHistoryAllSelector
from app.logic.models import (
    BalanceChangeReason,
    BalanceChangeType,
    BalanceChange,
)
from app.utils.dataclasses import object_to_dataclass
from .models import BalanceChangeModel


class SQLAlchemyBalanceHistoryStorage(
    BalanceHistoryEditor, BalanceHistoryAllSelector
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_balance(
        self,
        reason: BalanceChangeReason,
        created_at: datetime,
        user_id: int,
        balance: float,
    ) -> None:
        await self._change_balance(
            BalanceChangeType.add, created_at, reason, user_id, balance
        )
        return

    async def remove_balance(
        self,
        reason: BalanceChangeReason,
        created_at: datetime,
        user_id: int,
        balance: float,
    ) -> None:
        await self._change_balance(
            BalanceChangeType.remove, created_at, reason, user_id, balance
        )
        return

    async def set_balance(
        self,
        reason: BalanceChangeReason,
        created_at: datetime,
        user_id: int,
        balance: float,
    ) -> None:
        await self._change_balance(
            BalanceChangeType.set, created_at, reason, user_id, balance
        )
        return

    async def select_all_user_history(
        self, user_id: int
    ) -> list[BalanceChange]:
        stmt = select(BalanceChangeModel).where(
            BalanceChangeModel.user_id == user_id
        )
        res = await self._session.execute(stmt)
        return [
            object_to_dataclass(i, BalanceChange) for i in res.scalars().all()
        ]

    async def _change_balance(
        self,
        change_type: BalanceChangeType,
        created_at: datetime,
        reason: BalanceChangeReason,
        user_id: int,
        balance: float,
    ) -> None:
        stmt = insert(BalanceChangeModel).values(
            change_type=change_type,
            reason=reason,
            user_id=user_id,
            amount=balance,
            created_at=created_at,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return
