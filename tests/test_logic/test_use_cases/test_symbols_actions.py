from unittest.mock import AsyncMock
from datetime import datetime

from app.logic.use_cases.symbols_actions import (
    GetMySymbolsActions,
    MySymbolActionDTO,
)
from app.logic.models.symbol import SymbolAction, Action
from app.logic.dataclasses import objects_to_dataclasses


async def test_get_my_symbols_actions() -> None:
    USER_ID = 1234
    TICKER = "AAPL"
    RETURN_VALUE = [
        SymbolAction(USER_ID, TICKER, Action.buy, 9, 300.0, datetime.now()),
        SymbolAction(USER_ID, TICKER, Action.buy, 11, 299.5, datetime.now()),
        SymbolAction(USER_ID, TICKER, Action.sell, 20, 301.0, datetime.now()),
    ]
    symbols_actions = AsyncMock()
    symbols_actions.get_user_symbols_actions_by_symbol.return_value = (
        RETURN_VALUE
    )
    use_case = GetMySymbolsActions(symbols_actions)

    assert await use_case(USER_ID, TICKER) == objects_to_dataclasses(
        RETURN_VALUE, MySymbolActionDTO
    )
