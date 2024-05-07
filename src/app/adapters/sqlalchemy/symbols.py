from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import insert, update, exists, select

from app.logic.abstract import SymbolsStorage
from app.logic.models.symbol import Symbol, DEFAULT_AMOUNT
from app.utils.dataclasses import object_to_dataclass
from .models import SymbolModel


class SQLAlchemySymbolsStorage(SymbolsStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert_or_add(
        self, owner_id: int, code: str, amount: int
    ) -> None:
        if await self._exists(owner_id, code):
            await self._add(owner_id, code, amount)
            return
        await self._insert(owner_id, code, amount)

    async def get_amount(self, owner_id: int, code: str) -> int:
        stmt = select(SymbolModel.amount).where(
            SymbolModel.owner_id == owner_id, SymbolModel.code == code
        )
        try:
            res = (await self._session.execute(stmt)).scalar_one()
        except NoResultFound:
            res = DEFAULT_AMOUNT
        return res

    async def get_all_user_symbols(self, user_id: int) -> list[Symbol]:
        stmt = select(SymbolModel).where(SymbolModel.owner_id == user_id)
        res = await self._session.execute(stmt)
        return [object_to_dataclass(i, Symbol) for i in res.scalars().all()]

    async def remove(self, owner_id: int, code: str, amount: int) -> None:
        stmt = (
            update(SymbolModel)
            .values(amount=SymbolModel.amount - amount)
            .where(SymbolModel.owner_id == owner_id, SymbolModel.code == code)
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _insert(self, owner_id: int, code: str, amount: int) -> None:
        stmt = insert(SymbolModel).values(
            owner_id=owner_id, code=code, amount=amount
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _add(self, owner_id: int, code: str, amount: int) -> None:
        stmt = (
            update(SymbolModel)
            .values(amount=SymbolModel.amount + amount)
            .where(SymbolModel.owner_id == owner_id, SymbolModel.code == code)
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def _exists(self, owner_id: int, code: str) -> bool:
        stmt = (
            exists(SymbolModel)
            .where(SymbolModel.owner_id == owner_id, SymbolModel.code == code)
            .select()
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()
