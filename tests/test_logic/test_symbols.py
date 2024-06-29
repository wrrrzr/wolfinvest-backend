import pytest

from app.logic.abstract import SymbolsPriceGetter
from app.logic.use_cases.symbols import GetSymbol


class MockSymbolsPriceGetter(SymbolsPriceGetter):
    def __init__(self, values: dict[str, float]) -> None:
        self._values = values

    async def get_price(self, symbol: str) -> float:
        return self._values[symbol]


@pytest.mark.parametrize(
    "foo, bar", [[5.0, 121.0], [135.0, 135.0], [123.50, 0.0]]
)
async def test_get_symbol(foo: float, bar: float) -> None:
    use_case = GetSymbol(MockSymbolsPriceGetter({"FOO": foo, "BAR": bar}))
    assert await use_case("FOO") == foo
    assert await use_case("BAR") == bar
