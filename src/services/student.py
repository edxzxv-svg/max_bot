
from src.enums import RequestStatus, UserRole
from src.models import User
from src.repositories import StudentRepository, UserRepository
from src.schemes.request import (
    StudentListRequest,
)
from src.schemes.response import (
    StudentBrief,
    StudentListResponse,
)
from src.session import async_session_maker


class StudentService:
    def __init__(
            self,
            student_repo: StudentRepository,
            user_repo: UserRepository,
    ):
        self.student_repo = student_repo
        self.user_repo = user_repo

    async def get_list(
            self,
            params: StudentListRequest,
            user: User,
    ) -> StudentListResponse:
        async with async_session_maker() as session:
            match user.role:
                case UserRole.STUDENT:
                    student = await self.student_repo.get_by(
                        session, user_id=user.user_id
                    )
                    if not student:
                        return StudentListResponse(
                            status=RequestStatus.FAILED,
                            detail="Доступ запрещен"
                        )
                    params.class_numbers = [student.class_number]
                    params.class_parallels = [student.class_parallel]
                case UserRole.GUEST:
                    return StudentListResponse(
                        status=RequestStatus.FAILED,
                        detail="Доступ запрещен"
                    )

            result = await self.student_repo.get_list(
                session,
                first_names=params.first_names,
                last_names=params.last_names,
                second_names=params.second_names,
                start_date=params.start_date,
                end_date=params.end_date,
                class_numbers=params.class_numbers,
                class_parallels=params.class_parallels,
            )

            return StudentListResponse(
                status=RequestStatus.SUCCESS,
                data=[
                    StudentBrief(
                        full_name=(
                            f"{row.last_name} "
                            f"{row.first_name} "
                            f"{row.second_name}" if row.second_name else ""
                        ),
                        birth_day=row.birth_day,
                        class_number=row.class_number,
                        class_parallel=row.class_parallel,
                    )
                    for row in result
                ],
                detail=f"Найдено {len(result)}"
            )
