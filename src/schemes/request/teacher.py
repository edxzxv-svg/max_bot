
from datetime import UTC, date, datetime

from pydantic import BaseModel, Field, field_validator


class TeacherCreateRequest(BaseModel):
    user_uuid: int | None = Field(
        default=None,
        title="Идентификатор",
        description="UUID пользователя в системе",
        examples=[12345, 67890]
    )
    first_name: str = Field(
        title="Фамилия",
        description="Фамилия учителя",
        min_length=2,
        max_length=50,
        examples=["Иванова", "Петрова", "Сидорова"]
    )
    last_name: str = Field(
        title="Имя",
        description="Имя учителя",
        min_length=2,
        max_length=50,
        examples=["Мария", "Анна", "Елена"]
    )
    second_name: str | None = Field(
        default=None,
        title="Отчество",
        description="Отчество учителя",
        min_length=2,
        max_length=50,
        examples=["Ивановна", "Петровна"]
    )
    birth_day: date = Field(
        title="Дата рождения",
        description="Дата рождения",
        examples=["1980-01-15", "1975-05-20"]
    )
    employment_date: date | None = Field(
        default=None,
        title="Дата трудоустройства",
        description="Дата трудоустройства",
        examples=["2020-09-01", "2015-08-15"]
    )
    total_years_at_hire: int | None = Field(
        default=0,
        title="Общий стаж (лет)",
        description="Общий стаж (лет) на дату приема",
        ge=0,
        examples=[5, 10, 15]
    )
    total_months_at_hire: int | None = Field(
        default=0,
        title="Общий стаж (месяцев)",
        description="Общий стаж (месяцев) на дату приема",
        ge=0,
        le=11,
        examples=[3, 6, 9]
    )
    total_days_at_hire: int | None = Field(
        default=0,
        title="Общий стаж (дней)",
        description="Общий стаж (дней) на дату приема",
        ge=0,
        le=30,
        examples=[5, 15, 25]
    )
    teacher_years_at_hire: int | None = Field(
        default=0,
        title="Педагогический стаж (лет)",
        description="Педагогический стаж (лет) на дату приема",
        ge=0,
        examples=[3, 8, 12]
    )
    teacher_months_at_hire: int | None = Field(
        default=0,
        title="Педагогический стаж (месяцев)",
        description="Педагогический стаж (месяцев) на дату приема",
        ge=0,
        le=11,
        examples=[2, 5, 8]
    )
    teacher_days_at_hire: int | None = Field(
        default=0,
        title="Педагогический стаж (дней)",
        description="Педагогический стаж (дней) на дату приема",
        ge=0,
        le=30,
        examples=[3, 10, 20]
    )
    education: str | None = Field(
        default=None,
        title="Образование",
        description="Образование",
        max_length=50,
        examples=["Высшее педагогическое", "Среднее специальное"]
    )

    @field_validator("birth_day")
    @classmethod
    def validate_birth_day(cls, v: date) -> date:
        """Валидация даты рождения: не может быть в будущем."""
        if v > datetime.now(UTC).date():
            msg = "Дата рождения не может быть в будущем"
            raise ValueError(msg)
        return v

    @field_validator("employment_date")
    @classmethod
    def validate_employment_date(cls, v: date | None) -> date | None:
        """Валидация даты трудоустройства: не может быть в будущем."""
        if v and v > datetime.now(UTC).date():
            msg = "Дата трудоустройства не может быть в будущем"
            raise ValueError(msg)
        return v

    @field_validator("total_months_at_hire", "teacher_months_at_hire")
    @classmethod
    def validate_months(cls, v: int | None) -> int | None:
        """Валидация месяцев: от 0 до 11."""
        if v is not None and (v < 0 or v > 11): # noqa: PLR2004
            msg = "Количество месяцев должно быть от 0 до 11"
            raise ValueError(msg)
        return v

    @field_validator("total_days_at_hire", "teacher_days_at_hire")
    @classmethod
    def validate_days(cls, v: int | None) -> int | None:
        """Валидация дней: от 0 до 30."""
        if v is not None and (v < 0 or v > 30): # noqa: PLR2004
            msg = "Количество дней должно быть от 0 до 30"
            raise ValueError(msg)
        return v

class TeacherListRequest(BaseModel):
    first_names: list[str] | None = Field(
        default=None,
        title="Фамилия",
        description="Фамилия учителя",
        examples=["Булгаков", "Куликовских"],
    )
    last_names: list[str] | None =  Field(
        default=None,
        title="Имя",
        description="Имя учителя",
        examples=["Иван", "Мухамед", "Джон"],
    )
    second_names: list[str] | None =  Field(
        default=None,
        title="Отчество",
        description="Отчество учителя",
        examples=["Николаевич", "Иванович"],
    )
    birth_day_ge: date | None =  Field(
        default=None,
        title="Дата с",
        description="Начало периода поиска даты рождения",
        examples=["1954-01-01", "2020-12-31"],
    )
    birth_day_le: date | None =  Field(
        default=None,
        title="Дата по",
        description="конец периода поиска даты рождения",
        examples=["1954-01-01", "2020-12-31"],
    )
    employment_date_ge: date | None =  Field(
        default=None,
        title="Дата с",
        description="Начало периода поиска даты трудоустройства",
        examples=["1954-01-01", "2020-12-31"],
    )
    employment_date_le: date | None =  Field(
        default=None,
        title="Дата по",
        description="конец периода поиска даты трудоустройства",
        examples=["1954-01-01", "2020-12-31"],
    )
