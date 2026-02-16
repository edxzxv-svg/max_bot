
from emums import RequestStatus
from emums.persons import UserRole
from models import User
from repositories.user import UserRepository
from schemes.request import StudentListRequest
from repositories.student import StudentRepository
from schemes.response.student import StudentListResponse, StudentBrief
from session import async_session_maker


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
                    student = await self.student_repo.get_by(session, id=user.user_id)
                    if not student:
                        return StudentListResponse(
                            status=StudentListResponse.Status.FAILED,
                            detail="Доступ запрещен"
                        )
                    params.class_numbers = [student.class_number]
                    params.class_parallels = [student.class_parallel]
                case UserRole.GUEST:
                    return StudentListResponse(
                        status=StudentListResponse.Status.FAILED,
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
                    StudentBrief.model_validate(
                        StudentBrief(
                            full_name=f"{row.last_name} {row.first_name} {row.second_name}",
                            birth_day=row.birth_day,
                            class_number=row.class_number,
                            class_parallel=row.class_parallel,
                        )
                    )
                    for row in result
                ],
                detail=f"Найдено {len(result)}"
            )
