
from src.enums import RequestStatus, UserRole
from src.models import User
from src.repositories import ScheduleRepository, UserRepository
from src.schemes.request import ScheduleRequest
from src.schemes.response import (
    ScheduleResponse,
    ScheduleRow,
)
from src.session import async_session_maker


class ScheduleService:
    def __init__(
            self,
            schedule_repo: ScheduleRepository,
            user_repo: UserRepository,
    ):
        self.schedule_repo = schedule_repo
        self.user_repo = user_repo

    async def get_list(
            self,
            params: ScheduleRequest,
            user: User,
    ) -> ScheduleResponse:
        if user.role not in [
            UserRole.STUDENT,
            UserRole.TEACHER,
            UserRole.ADMIN
        ]:
            return ScheduleResponse(
                status=RequestStatus.FAILED,
                detail="Доступ запрещен"
            )

        async with async_session_maker() as session:
            result = await self.schedule_repo.get_list(
                session,
                class_numbers=params.class_numbers,
                class_parallels=params.class_parallels,
                lesson_numbers=params.lesson_numbers,
                day_of_weeks=params.day_of_weeks,
                subjects=params.subjects,
                rooms=params.rooms,
            )

            return ScheduleResponse(
                status=RequestStatus.SUCCESS,
                data=[
                    ScheduleRow(
                        class_number=row.class_number,
                        class_parallel=row.class_parallel,
                        lesson_number=row.lesson_number,
                        day_of_week=row.day_of_week,
                        subject=row.subject,
                        room=row.room,
                    )
                    for row in result
                ],
                detail=f"Найдено {len(result)}"
            )
