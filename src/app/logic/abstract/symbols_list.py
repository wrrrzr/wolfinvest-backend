from abc import ABC, abstractmethod

from app.logic.models import SymbolInList


class SymbolsList(ABC):
    @abstractmethod
    async def get_all(self) -> list[SymbolInList]:
        raise NotImplementedError
