import pytest

from app.logic.abstract import SymbolsPriceGetter
from app.logic.use_cases.symbols import GetSymbol
from app.logic.models import SymbolPrice


class MockSymbolsPriceGetter(SymbolsPriceGetter):
    def __init__(self, values: dict[str, SymbolPrice]) -> None:
        self._values = values

    async def get_price(self, symbol: str) -> SymbolPrice:
        return self._values[symbol]


@pytest.mark.parametrize(
    "foo, bar",
    [
        [SymbolPrice(5.0, 4.9), SymbolPrice(121.0, 120.1)],
        [SymbolPrice(135.0, 134.8), SymbolPrice(135.0, 143.8)],
        [SymbolPrice(123.50, 123.35), SymbolPrice(0.0, 0.0)],
    ],
)
async def test_get_symbol(foo: SymbolPrice, bar: SymbolPrice) -> None:
    use_case = GetSymbol(MockSymbolsPriceGetter({"FOO": foo, "BAR": bar}))
    assert await use_case("FOO") == foo
    assert await use_case("BAR") == bar
