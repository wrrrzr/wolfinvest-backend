from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, exists, delete

from app.utils.dataclasses import object_to_dataclass
from app.logic.abstract.currency_storage import CurrencyStorage
from app.logic.models.currency import Currency
from .models import CurrencyModel


class SQLAlchemyCurrencyStorage(CurrencyStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_user_currencies(self, user_id: int) -> list[Currency]:
        stmt = select(CurrencyModel).where(CurrencyModel.user_id == user_id)
        res = await self._session.execute(stmt)
        return [object_to_dataclass(i, Currency) for i in res.scalars().all()]

    async def insert_or_add(
        self, user_id: int, ticker: str, amount: float
    ) -> None:
        if await self._exists(user_id, ticker):
            await self._add(user_id, ticker, amount)
            return
        await self._insert(user_id, ticker, amount)

    async def delete_all_user_currencies(self, user_id: int) -> None:
        stmt = delete(CurrencyModel).where(CurrencyModel.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _insert(self, user_id: int, ticker: str, amount: float) -> None:
        stmt = insert(CurrencyModel).values(
            user_id=user_id, ticker=ticker, amount=amount
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _add(self, user_id: int, ticker: str, amount: float) -> None:
        stmt = (
            update(CurrencyModel)
            .values(amount=CurrencyModel.amount + amount)
            .where(
                CurrencyModel.user_id == user_id,
                CurrencyModel.ticker == ticker,
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _exists(self, user_id: int, ticker: str) -> bool:
        stmt = (
            exists(CurrencyModel)
            .where(
                CurrencyModel.user_id == user_id,
                CurrencyModel.ticker == ticker,
            )
            .select()
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()
