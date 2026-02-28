from uuid import UUID, uuid4

from sqlalchemy import Date, Integer, String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Student(Base):
    __tablename__ = "students"

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
