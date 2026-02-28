from uuid import UUID, uuid4
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Schedule(Base):
    __tablename__ = "schedule"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    class_number: Mapped[int] = mapped_column(
        Integer,
        comment="Номер класса",
    )
    class_parallel: Mapped[str] = mapped_column(
        String(1),
        comment="Параллель",
    )
    day_of_week: Mapped[int] = mapped_column(
        Integer,
        comment="День недели",
    )
    lesson_number: Mapped[int] = mapped_column(
        Integer,
        comment="Номер урока",
    )
    subject: Mapped[str] = mapped_column(
        String,
        comment="Предмет",
    )
    room: Mapped[int | None] = mapped_column(
        Integer,
        comment="Кабинет",
    )
