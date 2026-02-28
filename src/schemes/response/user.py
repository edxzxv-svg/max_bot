
from datetime import date, datetime
from pydantic import BaseModel, Field
from emums import RequestStatus
from emums.persons import UserRole, UserStatus


class UserResponse(BaseModel):
    name: str | None = Field(
        None,
        title="Имя",
        description="Имя пользователя",
        min_length=2,
        max_length=100,
    )
    role: UserRole = Field(
        title="Роль",
        description="Роль пользователя",
    )
    status: UserStatus = Field(
        title="Статус",
        description="Статус пользователя",
    )
    last_activity: datetime | None = Field(
        None,
        title="Последняя активность",
        description="УПоследняя активность",
    )

class UserListResponse(BaseModel):
    status: RequestStatus = Field(
        None,
        title="Статус",
        description="Статус запроса",
    )
    data: list[UserResponse] = Field(
        default_factory=list,
        title="Результат",
        description="Результат запроса",
    )
    detail: str | None = Field(
        None,
        title="Детали статуса",
        description="Детали статуса",
    )

class SetNameResponse(BaseModel):
    status: RequestStatus = Field(
        None,
        title="Статус",
        description="Статус запроса",
    )
    detail: str | None = Field(
        None,
        title="Детали статуса",
        description="Детали статуса",
    )