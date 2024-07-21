from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
