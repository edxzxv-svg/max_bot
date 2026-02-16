
from datetime import date
from pydantic import BaseModel, Field, field_validator


class StudentCreateRequest(BaseModel):
    """
    Pydantic модель для создания нового ученика.
    Все поля, кроме uuid и user_uuid, обязательны для заполнения.
    """

    # uuid генерируется автоматически на стороне сервера, поэтому не включаем в запрос

    first_name: str = Field(
        description="Фамилия ученика",
        min_length=2,
        max_length=50,
        examples=["Иванов", "Петров", "Сидоров"]
    )

    last_name: str = Field(
        description="Имя ученика",
        min_length=2,
        max_length=50,
        examples=["Иван", "Мария", "Алексей"]
    )

    second_name: str | None = Field(
        default=None,
        description="Отчество ученика",
        min_length=2,
        max_length=50,
        examples=["Иванович", "Петровна"]
    )

    birth_day: date = Field(
        description="Дата рождения ученика",
        examples=["2011-01-15", "2010-05-20"]
    )

    class_number: int = Field(
        description="Номер класса",
        ge=0,
        le=11,
        examples=[5, 8, 11]
    )

    class_parallel: str = Field(
        ...,
        description="Буква параллели класса",
        min_length=1,
        max_length=1,
        pattern=r'^[А-Яа-яA-Za-z]$',
        examples=["А", "Б", "В", "A", "B"]
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

class StudentListRequest(BaseModel):
    first_names: list[str] | None = Field(
        default=None,
        title="Фамилия",
        description="Фамилия человека",
        examples=["Булгаков", "Куликовских"],
    )
    last_names: list[str] | None =  Field(
        default=None,
        title="Имя",
        description="Имя человека",
        examples=["Иван", "Мухамед", "Джон"],
    )
    second_names: list[str] | None =  Field(
        default=None,
        title="Отчество",
        description="Отчество человека",
        examples=["Николаевич", "Иванович"],
    )
    start_date: date | None =  Field(
        default=None,
        title="Дата с",
        description="Начало периода поиска",
        examples=['1954-01-01', '2020-12-31'],
    )
    end_date: date | None =  Field(
        default=None,
        title="Дата по",
        description="конец периода поиска",
        examples=['1954-01-01', '2020-12-31'],
    )
    class_numbers: list[int] | None =  Field(
        default=None,
        title="Класс",
        description="Класс ученика",
        examples=[9, 8, 0],
    )
    class_parallels: list[str] | None =  Field(
        default=None,
        title="",
        description="",
        examples=[],
    )