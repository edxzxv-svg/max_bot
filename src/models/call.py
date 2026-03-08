from datetime import time
from uuid import UUID, uuid4

from sqlalchemy import Integer, Time
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Call(Base):
    __tablename__ = "calls"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    day_of_week: Mapped[int] = mapped_column(
        Integer,
        index=True,
        comment="День недели",
    )
    lesson_number: Mapped[int] = mapped_column(
        Integer,
        index=True,
        comment="Номер урока",
    )
    start_time: Mapped[time] = mapped_column(
        Time,
        index=True,
        comment="Время начала урока",
    )
    end_time: Mapped[time] = mapped_column(
        Time,
        index=True,
        comment="Время окончания урока",
    )
