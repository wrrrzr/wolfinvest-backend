from datetime import datetime, timezone

from app.logic.abstract.clock import Clock


class UTCClock(Clock):
    async def get_current_time(self) -> datetime:
        return datetime.now(timezone.utc)
