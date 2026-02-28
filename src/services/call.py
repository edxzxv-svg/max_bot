
from emums import RequestStatus
from emums.persons import UserRole
from models import User
from repositories import CallRepository
from repositories.user import UserRepository
from schemes.request import CallRequest
from schemes.response import CallResponse, CallRow
from schemes.response.student import StudentListResponse
from session import async_session_maker


class CallService:
    def __init__(
            self,
            call_repo: CallRepository,
            user_repo: UserRepository,
    ):
        self.call_repo = call_repo
        self.user_repo = user_repo

    async def get_list(
            self,
            params: CallRequest,
            user: User,
    ) -> CallResponse:
        if user.role not in [UserRole.STUDENT, UserRole.TEACHER, UserRole.ADMIN]:
            return CallResponse(
                status=StudentListResponse.Status.FAILED,
                detail="Доступ запрещен"
            )

        async with async_session_maker() as session:
            result = await self.call_repo.get_list(
                session,
                lesson_numbers=params.lesson_numbers,
                day_of_weeks=params.day_of_weeks,
                start_time_ge=params.start_time_ge,
                start_time_le=params.start_time_le,
                end_time_ge=params.end_time_ge,
                end_time_le=params.end_time_le,
            )

            return CallResponse(
                status=RequestStatus.SUCCESS,
                data=[
                    CallRow(
                        lesson_number=row.lesson_number,
                        day_of_week=row.day_of_week,
                        start_time=row.start_time,
                        end_time=row.end_time,
                    )
                    for row in result
                ],
                detail=f"Найдено {len(result)}"
            )
