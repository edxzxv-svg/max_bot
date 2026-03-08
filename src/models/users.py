from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[int] = mapped_column(
        unique=True,
        index=True,
        nullable=True,
    )
    name: Mapped[str | None] = mapped_column(
        String(50),
        index=True,
        comment="Имя пользователя",
    )
    role: Mapped[str] = mapped_column(
        String(50),
        index=True,
        comment="Роль пользователя",
    )
    status: Mapped[str] = mapped_column(
        String(10),
        index = True,
        comment = "Статус пользователя",
    )
    last_activity_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        index=True,
        comment="Дата и время последней активности пользователя",
    )
