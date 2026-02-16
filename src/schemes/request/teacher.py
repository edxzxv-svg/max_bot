
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TeacherCreateRequest(BaseModel):
    """
    Pydantic модель для создания нового учителя.
    Все поля, кроме user_uuid и education, обязательны для заполнения.
    """


    user_uuid: Optional[int] = Field(
        default=None,
        description="UUID пользователя в системе (если учитель зарегистрирован)",
        examples=[12345, 67890]
    )

    first_name: str = Field(
        description="Фамилия учителя",
        min_length=2,
        max_length=50,
        examples=["Иванова", "Петрова", "Сидорова"]
    )

    last_name: str = Field(
        description="Имя учителя",
        min_length=2,
        max_length=50,
        examples=["Мария", "Анна", "Елена"]
    )

    second_name: Optional[str] = Field(
        default=None,
        description="Отчество учителя",
        min_length=2,
        max_length=50,
        examples=["Ивановна", "Петровна"]
    )

    birth_day: date = Field(
        description="Дата рождения учителя",
        examples=["1980-01-15", "1975-05-20"]
    )

    employment_date: Optional[date] = Field(
        default=None,
        description="Дата трудоустройства",
        examples=["2020-09-01", "2015-08-15"]
    )

    total_years_at_hire: Optional[int] = Field(
        default=0,
        description="Общий стаж (лет) на дату приема",
        ge=0,
        examples=[5, 10, 15]
    )

    total_months_at_hire: Optional[int] = Field(
        default=0,
        description="Общий стаж (месяцев) на дату приема",
        ge=0,
        le=11,
        examples=[3, 6, 9]
    )

    total_days_at_hire: Optional[int] = Field(
        default=0,
        description="Общий стаж (дней) на дату приема",
        ge=0,
        le=30,
        examples=[5, 15, 25]
    )

    teacher_years_at_hire: Optional[int] = Field(
        default=0,
        description="Педагогический стаж (лет) на дату приема",
        ge=0,
        examples=[3, 8, 12]
    )

    teacher_months_at_hire: Optional[int] = Field(
        default=0,
        description="Педагогический стаж (месяцев) на дату приема",
        ge=0,
        le=11,
        examples=[2, 5, 8]
    )

    teacher_days_at_hire: Optional[int] = Field(
        default=0,
        description="Педагогический стаж (дней) на дату приема",
        ge=0,
        le=30,
        examples=[3, 10, 20]
    )

    education: Optional[str] = Field(
        default=None,
        description="Образование",
        max_length=50,
        examples=["Высшее педагогическое", "Среднее специальное"]
    )

    @field_validator('birth_day')
    @classmethod
    def validate_birth_day(cls, v: date) -> date:
        """
        Валидация даты рождения: не может быть в будущем
        """
        if v > date.today():
            raise ValueError('Дата рождения не может быть в будущем')
        return v

    @field_validator('employment_date')
    @classmethod
    def validate_employment_date(cls, v: Optional[date]) -> Optional[date]:
        """
        Валидация даты трудоустройства: не может быть в будущем
        """
        if v and v > date.today():
            raise ValueError('Дата трудоустройства не может быть в будущем')
        return v

    @field_validator('total_months_at_hire', 'teacher_months_at_hire')
    @classmethod
    def validate_months(cls, v: Optional[int]) -> Optional[int]:
        """
        Валидация месяцев: от 0 до 11
        """
        if v is not None and (v < 0 or v > 11):
            raise ValueError('Количество месяцев должно быть от 0 до 11')
        return v

    @field_validator('total_days_at_hire', 'teacher_days_at_hire')
    @classmethod
    def validate_days(cls, v: Optional[int]) -> Optional[int]:
        """
        Валидация дней: от 0 до 30
        """
        if v is not None and (v < 0 or v > 30):
            raise ValueError('Количество дней должно быть от 0 до 30')
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
        examples=['1954-01-01', '2020-12-31'],
    )
    birth_day_le: date | None =  Field(
        default=None,
        title="Дата по",
        description="конец периода поиска даты рождения",
        examples=['1954-01-01', '2020-12-31'],
    )
    employment_date_ge: date | None =  Field(
        default=None,
        title="Дата с",
        description="Начало периода поиска даты трудоустройства",
        examples=['1954-01-01', '2020-12-31'],
    )
    employment_date_le: date | None =  Field(
        default=None,
        title="Дата по",
        description="конец периода поиска даты трудоустройства",
        examples=['1954-01-01', '2020-12-31'],
    )