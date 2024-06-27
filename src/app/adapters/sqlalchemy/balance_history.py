from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.logic.abstract import BalanceHistoryStorage
from app.logic.models import (
    BalanceChangeReason,
    BalanceChangeType,
    BalanceChange,
)
from app.utils.dataclasses import object_to_dataclass
from .models import BalanceChangeModel


class SQLAlchemyBalanceHistoryStorage(BalanceHistoryStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        await self._change_balance(
            BalanceChangeType.add, reason, user_id, balance
        )
        return

    async def remove_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        await self._change_balance(
            BalanceChangeType.remove, reason, user_id, balance
        )
        return

    async def set_balance(
        self, reason: BalanceChangeReason, user_id: int, balance: float
    ) -> None:
        await self._change_balance(
            BalanceChangeType.set, reason, user_id, balance
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
        reason: BalanceChangeReason,
        user_id: int,
        balance: float,
    ) -> None:
        stmt = insert(BalanceChangeModel).values(
            change_type=change_type,
            reason=reason,
            user_id=user_id,
            amount=balance,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return
