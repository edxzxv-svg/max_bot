
from datetime import date

from pydantic import BaseModel, Field

from src.enums import RequestStatus


class StudentBrief(BaseModel):
    full_name: str = Field(
        title="ФИО",
        description="ФИО ученика",
        min_length=2,
        max_length=100,
    )
    class_number: int = Field(
        title="Класс",
        description="Класс ученика",
        ge=0,
        le=11,
    )
    class_parallel: str = Field(
        title="Параллель",
        description="Параллель класса",
        min_length=1,
        max_length=1,
    )
    birth_day: date = Field(
        title="Дата рождения",
        description="Дата рождения ученика",
    )

class StudentListResponse(BaseModel):
    status: RequestStatus | None = Field(
        default=None,
        title="Статус",
        description="Статус запроса",
    )
    data: list[StudentBrief] = Field(
        default_factory=list,
        title="Результат",
        description="Результат запроса",
    )
    detail: str | None = Field(
        default=None,
        title="Детали статуса",
        description="Детали статуса",
    )
