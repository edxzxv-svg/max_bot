from uuid import UUID, uuid4

from sqlalchemy import String, text, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
        comment="Unique UUID",
    )
    user_uuid: Mapped[int] = mapped_column(
        unique=True,
        nullable=True,
    )
    first_name = mapped_column(
        String(50),
        comment="Фамилия",
    )
    last_name = mapped_column(
        String(50),
        comment="Имя",
    )
    second_name = mapped_column(
        String(50),
        comment="Отчество",
    )
    birth_day = mapped_column(
        Date,
        comment="Дата рождения",
    )
    employment_date = mapped_column(
        Date,
        comment="Дата трудоустройства"
    )
    total_years_at_hire = mapped_column(
        Integer,
        comment="Общий стаж (лет) на дату приема"
    )
    total_months_at_hire = mapped_column(
        Integer,
        comment="Общий стаж (месяцев) на дату приема"
    )
    total_days_at_hire = mapped_column(
        Integer,
        comment="Общий стаж (дней) на дату приема"
    )
    teacher_years_at_hire = mapped_column(
        Integer,
        comment="Педагогический стаж (лет) на дату приема"
    )
    teacher_months_at_hire = mapped_column(
        Integer,
        comment="Педагогический стаж (месяцев) на дату приема"
    )
    teacher_days_at_hire = mapped_column(
        Integer,
        comment="Педагогический стаж (дней) на дату приема"
    )
    education = mapped_column(
        String(50),
        comment="Образование"
    )