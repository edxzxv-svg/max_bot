
from emums import RequestStatus
from emums.persons import UserRole
from models import User
from repositories import TeacherRepository
from repositories.user import UserRepository
from schemes.request import TeacherListRequest
from schemes.response import TeacherListResponse, TeacherResponse
from schemes.response.student import StudentListResponse
from session import async_session_maker


class TeacherService:
    def __init__(
            self,
            teacher_repo: TeacherRepository,
            user_repo: UserRepository,
    ):
        self.teacher_repo = teacher_repo
        self.user_repo = user_repo

    async def get_list(
            self,
            params: TeacherListRequest,
            user: User,
    ) -> TeacherListResponse:
        async with async_session_maker() as session:
            if user.role not in (UserRole.ADMIN, UserRole.TEACHER):
                return TeacherListResponse(
                    status=StudentListResponse.Status.FAILED,
                    detail="Доступ запрещен"
                )

            result = await self.teacher_repo.get_list(
                session,
                first_names=params.first_names,
                last_names=params.last_names,
                second_names=params.second_names,
                birth_day_ge=params.birth_day_ge,
                birth_day_le=params.birth_day_le,
                employment_date_ge=params.employment_date_ge,
                employment_date_le=params.employment_date_le,
            )

            return TeacherListResponse(
                status=RequestStatus.SUCCESS,
                data=[
                    TeacherResponse(
                        full_name=f"{row.last_name} {row.first_name} {row.second_name}",
                        birth_day=row.birth_day,
                        employment_date=row.employment_date,
                        education=row.education,
                    )
                    for row in result
                ],
                detail=f"Найдено {len(result)}"
            )
