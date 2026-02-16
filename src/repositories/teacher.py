from datetime import date, datetime, time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import  Teacher
from .base import BaseRepository


class TeacherRepository(BaseRepository[Teacher]):
    def __init__(self) -> None:
        super().__init__(Teacher)

    async def get_list(
            self,
            session: AsyncSession,
            first_names: list[str] | None = None,
            last_names: list[str] | None = None,
            second_names: list[str] | None = None,
            birth_day_ge: date | None = None,
            birth_day_le: date | None = None,
            employment_date_ge: date | None = None,
            employment_date_le: date | None = None,
    ) -> list[Teacher]:
        stmt = select(self.model)

        if first_names:
            stmt = stmt.where(self.model.first_name.in_(first_names))

        if last_names:
            stmt = stmt.where(self.model.last_name.in_(last_names))

        if second_names:
            stmt = stmt.where(self.model.second_name.in_(second_names))

        if birth_day_ge:
            stmt = stmt.where(self.model.birth_day >= birth_day_ge)

        if birth_day_le:
            stmt = stmt.where(self.model.birth_day <= datetime.combine(birth_day_le, time.max))

        if employment_date_ge:
            stmt = stmt.where(self.model.employment_date >= employment_date_ge)

        if employment_date_le:
            stmt = stmt.where(self.model.employment_date <= datetime.combine(employment_date_le, time.max))

        result = await session.execute(stmt)
        return result.scalars().all() if result else []