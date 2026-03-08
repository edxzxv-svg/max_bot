
from datetime import datetime

from pydantic import BaseModel, Field

from src.enums import UserRole, UserStatus


class SetNameRequest(BaseModel):
    user_id: int = Field(
        title="Идентификатор пользователя",
        description="Идентификатор пользователя",
        examples=["555", "666", "777"]
    )
    name: str = Field(
        title="Имя",
        description="Имя пользователя",
        min_length=2,
        max_length=100,
        examples=["Иванов Петр", "Петров Иван Матвеич", "Aleksandra"],
    )

class SetRoleRequest(BaseModel):
    user_id: int = Field(
        title="Идентификатор",
        description="Идентификатор пользователя",
        examples=["555", "666", "777"],
    )
    role: UserRole = Field(
        title="Роль",
        description="Роль пользователя",
        examples=list(UserRole),
    )

class UserListRequest(BaseModel):
    names:list[str] | None = Field(
        None,
        title="Имя",
        description="Имя пользователя",
        examples=["Иванов Петр", "Петров Иван Матвеич", "Aleksandra"],
    )
    roles: set[UserRole] | None  = Field(
        None,
        title="Роль",
        description="Роль пользователя",
        examples=list(UserRole),
    )
    statuses: set[UserStatus] | None  = Field(
        None,
        title="Состояние",
        description="Состояние пользователя",
        examples=list(UserStatus),
    )
    last_activity_ge: datetime | None = Field(
        default=None,
        title="Активность с",
        description="Минимальная дата и время с последней активности",
        examples=["2026-01-01"],
    )
    last_activity_le: datetime | None = Field(
        default=None,
        title="Активность по",
        description="Максимальная дата и время с последней активности",
        examples=["2026-03-01"],
    )
