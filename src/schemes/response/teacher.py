
from datetime import date

from pydantic import BaseModel, Field

from src.enums import RequestStatus


class TeacherResponse(BaseModel):
    full_name: str = Field(
        title="ФИО",
        description="ФИО учителя",
        min_length=2,
        max_length=100,
    )
    birth_day: date | None= Field(
        default=None,
        title="Дата рождения",
        description="Дата рождения учителя",
    )
    employment_date: date | None = Field(
        default=None,
        title="Дата трудоустройства",
        description="Дата трудоустройства учителя",
    )
    education: str | None = Field(
        default=None,
        title="Образование",
        description="Уровень образования",
        min_length=2,
        max_length=100,
    )

class TeacherListResponse(BaseModel):
    status: RequestStatus | None = Field(
        default=None,
        title="Статус",
        description="Статус запроса",
    )
    data: list[TeacherResponse] = Field(
        default_factory=list,
        title="Результат",
        description="Результат запроса",
    )
    detail: str | None = Field(
        default=None,
        title="Детали статуса",
        description="Детали статуса",
    )
