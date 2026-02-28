from uuid import UUID
from pydantic import BaseModel, Field


class ScheduleCreateRequest(BaseModel):
    uuid: UUID
    class_number: int
    class_parallel: str
    day_of_week: int
    lesson_number: int
    subject: str
    room: int | None

class ScheduleRequest(BaseModel):
    class_numbers: list[int] | None =  Field(
        default=None,
        title="Класс",
        description="Класс",
        examples=[9, 8, 0],
    )
    class_parallels: list[str] | None =  Field(
        default=None,
        title="Параллель",
        description="Параллель",
        examples=['А', 'Б', 'В'],
    )
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
    subjects: list[str] | None =  Field(
        default=None,
        title="Предмет",
        description="Предмет",
        examples=['Математика', 'Физика'],
    )
    rooms: list[int] | None =  Field(
        default=None,
        title="Кабинет",
        description="Кабинет",
        examples=['24', '8'],
    )