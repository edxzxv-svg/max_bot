from typing import Any

from commands.base import BaseCommand
from emums.persons import UserRole, UserStatus
from repositories.user import UserRepository
from session import async_session_maker


class UserListCommand(BaseCommand):
    id: str = "user_list"

    description: str = f"""
    Назначение: Возвращает список зарегистрированных пользователей.
    Параметры:
        last_time: datetime | None - Получить информацию только по пользователя? которые онлайн за последние last_time
        roles: Literal[{[_ for _ in UserRole]}] | None  - Список ролей пользователей
        states: Literal[{[_ for _ in UserStatus]}] | None  - Статусы пользователей
    Результат:
        list[User] - список пользователей
    """

    def __init__(self, users_repo: UserRepository):
        self.users_repo = users_repo

    async def execute(self, **kwargs: Any) -> Any:
        async with async_session_maker() as session:
            await self.users_repo.get_list(
                session,
                roles=kwargs.get['roles'],
                states=kwargs.get['states'],
                is_online=kwargs.get['is_online'],
            )

