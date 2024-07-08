import asyncio

from app.utils.funcs import get_current_time


async def test_get_current_time() -> None:
    old_time = get_current_time()
    await asyncio.sleep(0.01)
    assert old_time < get_current_time()
