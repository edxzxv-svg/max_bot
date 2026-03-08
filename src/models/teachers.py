from uuid import UUID, uuid4

from sqlalchemy import Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
        comment="Unique UUID",
    )
    user_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.uuid",
            comment="UUID пользователя"
        ),
        unique=True,
        nullable=True,
    )
    first_name = mapped_column(
        String(50),
        index=True,
        comment="Фамилия",
    )
    last_name = mapped_column(
        String(50),
        index=True,
        comment="Имя",
    )
    second_name = mapped_column(
        String(50),
        index=True,
        comment="Отчество",
    )
    birth_day = mapped_column(
        Date,
        index=True,
        comment="Дата рождения",
    )
    employment_date = mapped_column(
        Date,
        index=True,
        comment="Дата трудоустройства",
    )
    total_years_at_hire = mapped_column(
        Integer,
        index=True,
        comment="Общий стаж (лет) на дату приема",
    )
    total_months_at_hire = mapped_column(
        Integer,
        index=True,
        comment="Общий стаж (месяцев) на дату приема",
    )
    total_days_at_hire = mapped_column(
        Integer,
        index=True,
        comment="Общий стаж (дней) на дату приема"
    )
    teacher_years_at_hire = mapped_column(
        Integer,
        index=True,
        comment="Педагогический стаж (лет) на дату приема",
    )
    teacher_months_at_hire = mapped_column(
        Integer,
        index=True,
        comment="Педагогический стаж (месяцев) на дату приема",
    )
    teacher_days_at_hire = mapped_column(
        Integer,
        index=True,
        comment="Педагогический стаж (дней) на дату приема",
    )
    education = mapped_column(
        String(50),
        index=True,
        comment="Образование",
    )
