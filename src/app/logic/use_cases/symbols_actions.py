from dataclasses import dataclass
from datetime import datetime

from app.logic.abstract.storages.symbols import SymbolsActionsManySelector
from app.logic.dataclasses import objects_to_dataclasses


@dataclass
class MySymbolActionDTO:
    action: int
    amount: int
    price: float
    created_at: datetime


class GetMySymbolsActions:
    def __init__(self, symbols_actions: SymbolsActionsManySelector) -> None:
        self._symbols_actions = symbols_actions

    async def __call__(
        self, user_id: int, symbol: str
    ) -> list[MySymbolActionDTO]:
        symbol = symbol.upper()
        symbols = (
            await self._symbols_actions.get_user_symbols_actions_by_symbol(
                user_id, symbol
            )
        )
        return objects_to_dataclasses(symbols, MySymbolActionDTO)
