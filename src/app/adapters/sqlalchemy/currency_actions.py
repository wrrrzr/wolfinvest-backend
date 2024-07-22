from datetime import datetime

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.logic.abstract.currency_actions_storage import CurrencyActionsStorage
from app.logic.models.symbol import SymbolAction, Action
from app.utils.dataclasses import object_to_dataclass
from .models import CurrenciesActionModel


class SQLAlchemyCurrenciesActionsStorage(CurrencyActionsStorage):
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
        await self._insert(
            user_id, ticker, amount, price, created_at, Action.buy
        )

    async def insert_sell(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        created_at: datetime,
    ) -> None:
        await self._insert(
            user_id, ticker, amount, price, created_at, Action.sell
        )

    async def get_user_currencies_actions_by_currency(
        self, user_id: int, ticker: str
    ) -> list[SymbolAction]:
        stmt = select(CurrenciesActionModel).where(
            CurrenciesActionModel.user_id == user_id,
            CurrenciesActionModel.ticker == ticker,
        )
        res = await self._session.execute(stmt)
        return [
            object_to_dataclass(i, SymbolAction) for i in res.scalars().all()
        ]

    async def delete_all_user_currency_actions(self, user_id: int) -> None:
        stmt = delete(CurrenciesActionModel).where(
            CurrenciesActionModel.user_id == user_id
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _insert(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        created_at: datetime,
        action: int,
    ) -> None:
        stmt = insert(CurrenciesActionModel).values(
            user_id=user_id,
            ticker=ticker,
            amount=amount,
            price=price,
            created_at=created_at,
            action=action,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return
