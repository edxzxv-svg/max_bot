
from pydantic import BaseModel, Field

from src.enums import RequestStatus


class ScheduleRow(BaseModel):
    day_of_week: int = Field(
        title="День недели",
        description="День недели",
        ge=1,
        le=7,
    )
    lesson_number: int = Field(
        title="Номер урока",
        description="Номер урока",
        ge=1,
        le=24,
    )
    subject: str = Field(
        title="Предмет",
        description="Предмет",
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
    room: int | None = Field(
        title="Кабинет",
        description="Кабинет",
        ge=1,
    )
class ScheduleResponse(BaseModel):
    status: RequestStatus | None = Field(
        default=None,
        title="Статус",
        description="Статус запроса",
    )
    data: list[ScheduleRow] = Field(
        default_factory=list,
        title="Результат",
        description="Результат запроса",
    )
    detail: str | None = Field(
        default=None,
        title="Детали статуса",
        description="Детали статуса",
    )
