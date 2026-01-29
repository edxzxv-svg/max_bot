from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[int] = mapped_column(
        unique=True,
        nullable=True,
    )
    name: Mapped[str | None] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(10))
    last_activity_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )
