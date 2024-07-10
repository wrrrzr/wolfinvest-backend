from datetime import datetime

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.logic.abstract.symbols_actions_storage import SymbolsActionsStorage
from app.logic.models.symbol import SymbolAction, Action
from app.utils.dataclasses import object_to_dataclass
from .models import SymbolActionModel


class SQLAlchemySymbolsActionsStorage(SymbolsActionsStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert_buy(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        created_at: datetime,
    ) -> None:
        stmt = insert(SymbolActionModel).values(
            user_id=user_id,
            ticker=ticker,
            amount=amount,
            price=price,
            created_at=created_at,
            action=Action.buy,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def insert_sell(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        created_at: datetime,
    ) -> None:
        stmt = insert(SymbolActionModel).values(
            user_id=user_id,
            ticker=ticker,
            amount=amount,
            price=price,
            created_at=created_at,
            action=Action.sell,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def get_user_symbols_actions_by_symbol(
        self, user_id: int, symbol: str
    ) -> list[SymbolAction]:
        stmt = select(SymbolActionModel).where(
            SymbolActionModel.user_id == user_id,
            SymbolActionModel.ticker == symbol,
        )
        res = await self._session.execute(stmt)
        return [
            object_to_dataclass(i, SymbolAction) for i in res.scalars().all()
        ]

    async def delete_all_user_symbols_actions(self, user_id: int) -> None:
        stmt = delete(SymbolActionModel).where(
            SymbolActionModel.user_id == user_id
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return
