from collections.abc import Sequence
from datetime import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Call

from .base import BaseRepository


class CallRepository(BaseRepository[Call]):
    def __init__(self) -> None:
        super().__init__(Call)

    async def get_list( # noqa: PLR0913
            self,
            session: AsyncSession,
            day_of_weeks: list[int] | None = None,
            lesson_numbers: list[int] | None = None,
            start_time_ge: time | None = None,
            start_time_le: time | None = None,
            end_time_ge: time | None = None,
            end_time_le: time | None = None,
    ) -> Sequence[Call]:
        stmt = select(self.model)

        if day_of_weeks:
            stmt = stmt.where(self.model.day_of_week.in_(day_of_weeks))

        if lesson_numbers:
            stmt = stmt.where(self.model.lesson_number.in_(lesson_numbers))

        if start_time_ge:
            stmt = stmt.where(self.model.start_time >= start_time_ge)

        if start_time_le:
            stmt = stmt.where(self.model.start_time <= start_time_le)

        if end_time_ge:
            stmt = stmt.where(self.model.end_time >= end_time_ge)

        if end_time_le:
            stmt = stmt.where(self.model.end_time <= end_time_le)

        result = await session.execute(stmt)
        return result.scalars().all() if result else []
