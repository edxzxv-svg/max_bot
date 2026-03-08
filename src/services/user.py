
from src.enums import RequestStatus, UserRole
from src.models import User
from src.repositories import UserRepository
from src.schemes.request import UserListRequest
from src.schemes.response import (
    UserListResponse,
    UserResponse,
)
from src.session import async_session_maker


class UserService:
    def __init__(
            self,
            user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    async def get_list(
            self,
            params: UserListRequest,
            user: User,
    ) -> UserListResponse:
        async with async_session_maker() as session:
            if user.role != UserRole.ADMIN:
                return UserListResponse(
                    status=RequestStatus.FAILED,
                    detail="Доступ запрещен"
                )

            result = await self.user_repo.get_list(
                session,
                roles=params.roles,
                states=params.statuses,
                last_activity_ge=params.last_activity_ge,
                last_activity_le=params.last_activity_le,
            )

            return UserListResponse(
                status=RequestStatus.SUCCESS,
                data=[
                    UserResponse.model_validate(row, from_attributes=True)
                    for row in result
                ],
                detail=f"Найдено {len(list(result))}"
            )
