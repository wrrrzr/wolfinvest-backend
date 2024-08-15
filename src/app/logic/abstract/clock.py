from abc import ABC, abstractmethod
from datetime import datetime


class ClockCurrentTimeGetter(ABC):
    @abstractmethod
    async def get_current_time(self) -> datetime:
        raise NotImplementedError


class Clock(ClockCurrentTimeGetter, ABC):
    pass
