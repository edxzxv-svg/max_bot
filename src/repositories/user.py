from datetime import datetime, UTC
from typing import Iterable, Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from emums.persons import UserRole, UserStatus
from src.models import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_list(
            self,
            session: AsyncSession,
            roles: set[UserRole] | None = None,
            states: set[UserStatus] | None = None,
            last_activity: datetime | None = None,
            **kwargs: Any,
    ) -> Iterable[User]:
        stmt = select(self.model).filter_by(**kwargs)

        if roles:
            stmt = stmt.where(self.model.role.in_(roles))

        if states:
            stmt = stmt.where(self.model.status.in_(states))

        if last_activity:
            now = datetime.now(UTC)
            delta = now - last_activity

            stmt = stmt.where(
                and_(
                    self.model.last_activity_at.isnot(None),
                    self.model.last_activity_at >= func.now() - func.interval(f'{delta} seconds')
                )
            )

        instances = await session.execute(stmt)
        return instances.scalars().all()