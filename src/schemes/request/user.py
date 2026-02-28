
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator

from emums.persons import UserRole, UserStatus


class SetNameRequest(BaseModel):
    user_id: int = Field(
        title="Идентификатор пользователя",
        description="Идентификатор пользователя",
        examples=["Иван", "Мария", "Алексей"]
    )
    name: str = Field(
        title="Имя",
        description="Имя пользователя",
        min_length=2,
        max_length=100,
        examples=["Иванов Петр", "Петров Иван Матвеич", "Aleksandra"]
    )

class SetRoleRequest(BaseModel):
    user_id: int = Field(
        title="Идентификатор пользователя",
        description="Идентификатор пользователя",
        examples=["Иван", "Мария", "Алексей"]
    )
    role: str = Field(
        title="Имя",
        description="Имя пользователя",
        min_length=2,
        max_length=100,
        examples=["Иванов Петр", "Петров Иван Матвеич", "Aleksandra"]
    )

class UserListRequest(BaseModel):
    names:list[str] | None = Field(
        None,
        title="Имя",
        description="Имя пользователя",
    )
    roles: list[UserRole] | None  = Field(
        None,
        title="Роль",
        description="Роль пользователя",
    )
    statuses: list[UserStatus] | None  = Field(
        None,
        title="Состояние",
        description="Состояние пользователя",
    )
    last_activity_ge: datetime = Field(
        None,
        title="Активность с",
        description="Минимальная дата и время с последней активности",
    )
    last_activity_le: datetime = Field(
        None,
        title="Активность по",
        description="Максимальная дата и время с последней активности",
    )
