from app.adapters.symbols_list import StaticSymbolsList


async def test_static() -> None:
    first_list = StaticSymbolsList()
    res1 = await first_list.get_all()
    res2 = await first_list.get_all()
    assert res1 == res2


async def test_single_result_for_all_lists() -> None:
    first_list = StaticSymbolsList()
    second_list = StaticSymbolsList()
    first_res = await first_list.get_all()
    second_res = await second_list.get_all()
    assert first_res == second_res
