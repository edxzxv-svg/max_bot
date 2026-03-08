from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from src.enums import UserRole, UserStatus
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
            last_activity_ge: datetime | None = None,
            last_activity_le: datetime | None = None,
            **kwargs: Any,
    ) -> Iterable[User]:
        stmt = select(self.model).filter_by(**kwargs)

        if roles:
            stmt = stmt.where(self.model.role.in_(roles))

        if states:
            stmt = stmt.where(self.model.status.in_(states))

        if last_activity_ge:
            now = datetime.now(UTC)
            delta = now - last_activity_ge

            stmt = stmt.where(
                and_(
                    self.model.last_activity_at.isnot(None),
                    self.model.last_activity_at >= (
                            func.now() - func.interval(f"{delta} seconds")
                    )
                )
            )

        if last_activity_le:
            now = datetime.now(UTC)
            delta = now - last_activity_le

            stmt = stmt.where(
                and_(
                    self.model.last_activity_at.isnot(None),
                    self.model.last_activity_at <= (
                            func.now() - func.interval(f"{delta} seconds")
                    )
                )
            )

        instances = await session.execute(stmt)
        return instances.scalars().all()
