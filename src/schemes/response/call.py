
from datetime import time

from pydantic import BaseModel, Field

from src.enums import RequestStatus


class CallRow(BaseModel):
    day_of_week: int = Field(
        title="День недели",
        description="День недели",
        ge=1,
        le=7,
    )
    lesson_number: int = Field(
        title="Номер урока",
        description="Номер урока",
        ge=0,
        le=24,
    )
    start_time: time = Field(
        title="Начало урока",
        description="Время начала урока",
    )
    end_time: time = Field(
        title="Конец урока",
        description="Время окочания урока",
    )


class CallResponse(BaseModel):
    status: RequestStatus | None = Field(
        default=None,
        title="Статус",
        description="Статус запроса",
    )
    data: list[CallRow] = Field(
        default_factory=list,
        title="Результат",
        description="Результат запроса",
    )
    detail: str | None = Field(
        default=None,
        title="Детали статуса",
        description="Детали статуса",
    )
