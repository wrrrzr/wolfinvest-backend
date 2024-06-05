from app.logic.abstract import SymbolsGetter
from app.adapters.symbols_list import StaticSymbolsList

MOCK_PRICE = 0.0


class MockSymbolsGetter(SymbolsGetter):
    async def get_price(self, symbol: str) -> float:
        return MOCK_PRICE

    async def get_daily_history(self, symbol: str) -> list[float]:
        pass


async def test_get_price() -> None:
    symbols_list = StaticSymbolsList(MockSymbolsGetter())
    assert (await symbols_list.get_all())[0].price == MOCK_PRICE


async def test_static() -> None:
    first_list = StaticSymbolsList(MockSymbolsGetter())
    res1 = await first_list.get_all()
    res2 = await first_list.get_all()
    assert res1 == res2


async def test_single_result_for_all_lists() -> None:
    first_list = StaticSymbolsList(MockSymbolsGetter())
    second_list = StaticSymbolsList(MockSymbolsGetter())
    first_res = await first_list.get_all()
    second_res = await second_list.get_all()
    assert first_res == second_res
