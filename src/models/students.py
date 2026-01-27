from uuid import UUID, uuid4

from sqlalchemy import String, text, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class Student(Base):
    __tablename__ = "students"

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
    class_number = mapped_column(
        Integer,
        comment="Номер класса",
    )
    class_parallel = mapped_column(
        String(1),
        comment="Параллель",
    )