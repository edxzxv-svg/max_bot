from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import  Schedule
from .base import BaseRepository


class ScheduleRepository(BaseRepository[Schedule]):
    def __init__(self) -> None:
        super().__init__(Schedule)

    async def get_list(
            self,
            session: AsyncSession,
            class_numbers: list[int] | None = None,
            class_parallels: list[str] | None = None,
            day_of_weeks: list[int] | None = None,
            lesson_numbers: list[int] | None = None,
            subjects: list[str] | None = None,
            rooms: list[int] | None = None,
    ) -> list[Schedule]:
        stmt = select(self.model)

        if class_numbers:
            stmt = stmt.where(self.model.class_number.in_(class_numbers))

        if class_parallels:
            stmt = stmt.where(self.model.class_parallel.in_(class_parallels))

        if day_of_weeks:
            stmt = stmt.where(self.model.day_of_week.in_(day_of_weeks))

        if lesson_numbers:
            stmt = stmt.where(self.model.lesson_number.in_(lesson_numbers))

        if subjects:
            stmt = stmt.where(self.model.subject.in_(subjects))

        if rooms:
            stmt = stmt.where(self.model.room.in_(rooms))

        result = await session.execute(stmt)
        return result.scalars().all() if result else []