from dataclasses import dataclass
from datetime import timedelta

from app.logic.abstract import SymbolsList
from app.logic.models import SymbolInList
from app.utils.funcs import get_current_time

TIME_EXP_CACHE = timedelta(minutes=10)


@dataclass
class MemorySymbolsList:
    data: list[SymbolInList]
    time_exp_cache: timedelta


def create_symbols_list_memory() -> MemorySymbolsList:
    return MemorySymbolsList([], get_current_time())


class SymbolsListCache(SymbolsList):
    def __init__(self, inner: SymbolsList, memory: MemorySymbolsList) -> None:
        self._inner = inner
        self._memory = memory

    async def get_all(self) -> list[SymbolInList]:
        if self._memory.time_exp_cache < get_current_time():
            self._memory.data = await self._inner.get_all()
            self._memory.time_exp_cache = get_current_time() + TIME_EXP_CACHE
        return self._memory.data
