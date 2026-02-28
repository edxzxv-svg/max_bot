from datetime import time
from uuid import UUID
from pydantic import BaseModel, Field


class CallRequest(BaseModel):
    day_of_weeks: list[int] | None =  Field(
        default=None,
        title="День недели",
        description="День недели",
        examples=[1, 2, 3],
    )
    lesson_numbers: list[int] | None =  Field(
        default=None,
        title="Номер урока",
        description="Номер урока",
        examples=[1, 2, 3],
    )
    start_time_ge: time | None =  Field(
        default=None,
        description="Время начала урока с",
        examples=['8:00', '9:45'],
    )
    start_time_le: time | None =  Field(
        default=None,
        description="Время начала урока по",
        examples=['10:10', '11:00'],
    )
    end_time_ge: time | None =  Field(
        default=None,
        description="Время окончания урока с",
        examples=['8:00', '9:45'],
    )
    end_time_le: time | None =  Field(
        default=None,
        description="Время окончания урока по",
        examples=['10:10', '11:00'],
    )