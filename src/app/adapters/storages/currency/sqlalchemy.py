from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, func, case

from app.logic.abstract.storages.currency import CurrencyStorage
from app.logic.models.currency import (
    CurrencyAction,
    Action,
    UserCurrencyData,
    CurrencyChange,
)
from app.logic.dataclasses import objects_to_dataclasses
from app.adapters.sqlalchemy.models import CurrenciesActionModel


class SQLAlchemyCurrencyStorage(CurrencyStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_amount(self, user_id: int, ticker: str) -> float:
        stmt = select(
            func.sum(
                case(
                    (
                        CurrenciesActionModel.action == Action.add,
                        CurrenciesActionModel.amount,
                    ),
                    (
                        CurrenciesActionModel.action == Action.remove,
                        -CurrenciesActionModel.amount,
                    ),
                    else_=0,
                )
            )
        ).where(
            CurrenciesActionModel.user_id == user_id,
            CurrenciesActionModel.ticker == ticker,
        )

        res = (await self._session.execute(stmt)).scalar()

        if res is not None:
            return res

        return 0.0

    async def get_all_user_currencies(
        self, user_id: int
    ) -> dict[str, UserCurrencyData]:
        stmt_actions = select(
            CurrenciesActionModel.ticker,
            CurrenciesActionModel,
        ).where(CurrenciesActionModel.user_id == user_id)

        stmt = (
            select(
                CurrenciesActionModel.ticker,
                func.sum(
                    case(
                        (
                            CurrenciesActionModel.action == Action.add,
                            CurrenciesActionModel.amount,
                        ),
                        (
                            CurrenciesActionModel.action == Action.remove,
                            -CurrenciesActionModel.amount,
                        ),
                        else_=0,
                    )
                ),
            )
            .where(CurrenciesActionModel.user_id == user_id)
            .group_by(CurrenciesActionModel.ticker)
        )

        res = (await self._session.execute(stmt)).all()
        list_actions = (await self._session.execute(stmt_actions)).all()
        res_actions = {}

        for i in list_actions:
            if i not in res_actions:
                res_actions[i[0]] = []
            res_actions[i[0]].append(i[1])

        return {
            symbols[0]: UserCurrencyData(
                amount=symbols[1],
                actions=objects_to_dataclasses(
                    res_actions[symbols[0]],
                    CurrencyAction,
                ),
            )
            for symbols in res
        }

    async def add(
        self,
        user_id: int,
        ticker: str,
        amount: float,
        price: float,
        created_at: datetime,
        reason: int,
    ) -> None:
        await self._insert(
            user_id,
            ticker,
            amount,
            price,
            created_at,
            Action.add,
            reason,
        )

    async def remove(
        self,
        user_id: int,
        ticker: str,
        amount: float,
        price: float,
        created_at: datetime,
        reason: int,
    ) -> None:
        await self._insert(
            user_id,
            ticker,
            amount,
            price,
            created_at,
            Action.remove,
            reason,
        )

    async def get_user_currencies_actions_by_currency(
        self, user_id: int, ticker: str
    ) -> list[CurrencyAction]:
        stmt = select(CurrenciesActionModel).where(
            CurrenciesActionModel.user_id == user_id,
            CurrenciesActionModel.ticker == ticker,
        )
        res = await self._session.execute(stmt)
        return objects_to_dataclasses(res.scalars().all(), CurrencyAction)

    async def get_all_user_currency_changes(
        self, user_id: int
    ) -> list[CurrencyChange]:
        stmt = (
            select(CurrenciesActionModel)
            .where(CurrenciesActionModel.user_id == user_id)
            .order_by(CurrenciesActionModel.created_at)
        )
        res = await self._session.execute(stmt)
        return objects_to_dataclasses(res.scalars().all(), CurrencyChange)

    async def delete_all_user_currencies(self, user_id: int) -> None:
        stmt = delete(CurrenciesActionModel).where(
            CurrenciesActionModel.user_id == user_id
        )
        await self._session.execute(stmt)
        return

    async def _insert(
        self,
        user_id: int,
        ticker: str,
        amount: float,
        price: float,
        created_at: datetime,
        action: int,
        reason: int,
    ) -> None:
        stmt = insert(CurrenciesActionModel).values(
            user_id=user_id,
            ticker=ticker,
            amount=amount,
            price=price,
            created_at=created_at,
            action=action,
            reason=reason,
        )
        await self._session.execute(stmt)
        return
