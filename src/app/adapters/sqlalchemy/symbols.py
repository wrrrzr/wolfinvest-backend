from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, exists

from app.logic.abstract import SymbolsStorage
from .models import SymbolModel


class SQLAlchemSymbolsStorage(SymbolsStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert_or_add(
        self, owner_id: int, code: str, amount: int
    ) -> None:
        if await self._exists_by_owner_id(owner_id):
            await self._add(owner_id, code, amount)
            return
        await self._insert(owner_id, code, amount)

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

    async def _exists_by_owner_id(self, owner_id: int) -> bool:
        stmt = (
            exists(SymbolModel)
            .where(SymbolModel.owner_id == owner_id)
            .select()
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()
