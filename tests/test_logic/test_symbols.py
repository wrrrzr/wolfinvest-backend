from typing import Optional

import pytest

from app.logic.abstract import SymbolsStorage
from app.logic.symbols import GetSymbol


class MockSymbolsStorage(SymbolsStorage):
    def __init__(self, value: Optional[float]) -> None:
        self._value = value

    async def get_price_or_none(self, symbol: str) -> Optional[float]:
        return self._value


@pytest.mark.parametrize("value", [5.0, None, 123.50])
async def test_get_symbol(value: Optional[float]) -> None:
    use_case = GetSymbol(MockSymbolsStorage(value))
    assert await use_case("FOO") == value
