from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, func, case

from app.logic.abstract.storages.symbols import SymbolsStorage
from app.logic.models.symbol import SymbolAction, Action, UserSymbolData
from app.logic.dataclasses import objects_to_dataclasses
from app.adapters.sqlalchemy.models import SymbolActionModel


class SQLAlchemySymbolsStorage(SymbolsStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        current_time: datetime,
    ) -> None:
        await self._insert(
            user_id, ticker, amount, price, current_time, Action.buy
        )
        return

    async def remove(
        self,
        user_id: int,
        ticker: str,
        amount: int,
        price: float,
        current_time: datetime,
    ) -> None:
        await self._insert(
            user_id, ticker, amount, price, current_time, Action.sell
        )
        return

    async def get_amount(self, user_id: int, ticker: str) -> int:
        stmt = select(
            func.sum(
                case(
                    (
                        SymbolActionModel.action == Action.buy,
                        SymbolActionModel.amount,
                    ),
                    (
                        SymbolActionModel.action == Action.sell,
                        -SymbolActionModel.amount,
                    ),
                    else_=0,
                )
            )
        ).where(SymbolActionModel.user_id == user_id)

        res = (await self._session.execute(stmt)).scalar_one()
        if res is not None:
            return res
        return 0

    async def get_all_user_symbols(
        self, user_id: int
    ) -> dict[str, UserSymbolData]:
        stmt_actions = select(
            SymbolActionModel.ticker,
            SymbolActionModel,
        ).where(SymbolActionModel.user_id == user_id)

        stmt = (
            select(
                SymbolActionModel.ticker,
                func.sum(
                    case(
                        (
                            SymbolActionModel.action == Action.buy,
                            SymbolActionModel.amount,
                        ),
                        (
                            SymbolActionModel.action == Action.sell,
                            -SymbolActionModel.amount,
                        ),
                        else_=0,
                    )
                ),
            )
            .where(SymbolActionModel.user_id == user_id)
            .group_by(SymbolActionModel.ticker)
        )

        res = (await self._session.execute(stmt)).all()
        list_actions = (await self._session.execute(stmt_actions)).all()
        res_actions = {}

        for i in list_actions:
            if i not in res_actions:
                res_actions[i[0]] = []
            res_actions[i[0]].append(i[1])

        return {
            symbols[0]: UserSymbolData(
                amount=symbols[1],
                actions=objects_to_dataclasses(
                    res_actions[symbols[0]], SymbolAction
                ),
            )
            for symbols in res
        }

    async def get_user_symbols_actions_by_symbol(
        self, user_id: int, ticker: str
    ) -> list[SymbolAction]:
        stmt = select(SymbolActionModel).where(
            SymbolActionModel.user_id == user_id,
            SymbolActionModel.ticker == ticker,
        )
        res = await self._session.execute(stmt)
        return objects_to_dataclasses(res.scalars().all(), SymbolAction)

    async def delete_all_user_symbols(self, user_id: int) -> None:
        stmt = delete(SymbolActionModel).where(
            SymbolActionModel.user_id == user_id
        )
        await self._session.execute(stmt)
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
        stmt = insert(SymbolActionModel).values(
            user_id=user_id,
            ticker=ticker,
            amount=amount,
            price=price,
            created_at=created_at,
            action=action,
        )
        await self._session.execute(stmt)
        return
