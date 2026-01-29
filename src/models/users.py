from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime
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
    name: Mapped[str | None] = mapped_column(
        String(50)
    )
    role: Mapped[str] = mapped_column(
        String(50)
    )
    status: Mapped[str] = mapped_column(
        String(10)
    )
    last_activity_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    def __repr__(self) -> str:
        return (
            f"<User: uuid:{self.uuid} telegram_id:{self.telegram_id} "
            f"name:{self.name} status:{self.status} "
            f"create_at:{self.created_at} update_at:{self.updated_at}>"
        )

