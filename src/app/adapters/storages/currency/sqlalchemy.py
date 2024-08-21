from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, func, case

from app.logic.abstract.storages.currency import CurrencyStorage
from app.logic.models.currency import (
    CurrencyAction,
    Action,
    UserCurrencyData,
    CurrencyChange,
    Reason,
    CurrencySymbolInfo,
)
from app.logic.dataclasses import object_to_dataclass, objects_to_dataclasses
from app.adapters.sqlalchemy.models import (
    CurrenciesActionModel,
    CurrencySymbolInfoModel,
)


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
        **additional_info: Any,
    ) -> None:
        await self._insert(
            user_id,
            ticker,
            amount,
            price,
            created_at,
            Action.add,
            reason,
            **additional_info,
        )

    async def remove(
        self,
        user_id: int,
        ticker: str,
        amount: float,
        price: float,
        created_at: datetime,
        reason: int,
        **additional_info: Any,
    ) -> None:
        await self._insert(
            user_id,
            ticker,
            amount,
            price,
            created_at,
            Action.remove,
            reason,
            **additional_info,
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
            select(CurrenciesActionModel, CurrencySymbolInfoModel)
            .where(CurrenciesActionModel.user_id == user_id)
            .order_by(CurrenciesActionModel.created_at)
            .outerjoin(
                CurrencySymbolInfoModel,
                CurrencySymbolInfoModel.currency_action
                == CurrenciesActionModel.id,
            )
        )
        stmt_res = await self._session.execute(stmt)
        res = []
        for change, symbol_info in stmt_res:
            additional_info = {}

            if symbol_info is not None:
                additional_info["symbol_info"] = object_to_dataclass(
                    symbol_info, CurrencySymbolInfo
                )

            i = CurrencyChange(
                ticker=change.ticker,
                amount=change.amount,
                reason=change.reason,
                created_at=change.created_at,
                additional_info=additional_info,
            )
            res.append(i)
        return res

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
        **additional_info: Any,
    ) -> None:
        stmt = (
            insert(CurrenciesActionModel)
            .values(
                user_id=user_id,
                ticker=ticker,
                amount=amount,
                price=price,
                created_at=created_at,
                action=action,
                reason=reason,
            )
            .returning(CurrenciesActionModel.id)
        )
        res = await self._session.execute(stmt)

        if reason in (Reason.buy_symbol, Reason.sell_symbol):
            symbol_info: CurrencySymbolInfo = additional_info["symbol_info"]
            symbol_info_stmt = insert(CurrencySymbolInfoModel).values(
                currency_action=res.scalar(),
                symbol_ticker=symbol_info.ticker,
                symbol_amount=symbol_info.amount,
            )
            await self._session.execute(symbol_info_stmt)
        return
