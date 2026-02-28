from datetime import date, datetime, time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Student
from .base import BaseRepository


class StudentRepository(BaseRepository[Student]):
    def __init__(self) -> None:
        super().__init__(Student)

    async def get_list(
            self,
            session: AsyncSession,
            first_names: list[str] | None = None,
            last_names: list[str] | None = None,
            second_names: list[str] | None = None,
            start_date: date | None = None,
            end_date: date | None = None,
            class_numbers: list[int] | None = None,
            class_parallels: list[str] | None = None,
    ) -> list[Student]:
        stmt = select(self.model)

        if first_names:
            stmt = stmt.where(self.model.first_name.in_(first_names))

        if last_names:
            stmt = stmt.where(self.model.last_name.in_(last_names))

        if second_names:
            stmt = stmt.where(self.model.second_name.in_(second_names))

        if start_date:
            stmt = stmt.where(self.model.birth_day >= start_date)

        if end_date:
            stmt = stmt.where(self.model.birth_day <= datetime.combine(end_date, time.max))

        if class_numbers:
            stmt = stmt.where(self.model.class_number.in_(class_numbers))

        if class_parallels:
            stmt = stmt.where(self.model.class_parallel.in_(class_parallels))

        result = await session.execute(stmt)
        return result.scalars().all() if result else []