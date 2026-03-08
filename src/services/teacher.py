
from src.enums import RequestStatus, UserRole
from src.models import User
from src.repositories import TeacherRepository, UserRepository
from src.schemes.request import TeacherListRequest
from src.schemes.response import TeacherListResponse, TeacherResponse
from src.session import async_session_maker


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
                    status=RequestStatus.FAILED,
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
                        full_name=(
                            f"{row.last_name} "
                            f"{row.first_name} "
                            f"{row.second_name}" if row.second_name else ""
                        ),
                        birth_day=row.birth_day,
                        employment_date=row.employment_date,
                        education=row.education,
                    )
                    for row in result
                ],
                detail=f"Найдено {len(result)}"
            )
