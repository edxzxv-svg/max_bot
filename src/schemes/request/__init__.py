from .student import StudentListRequest, StudentCreateRequest
from .teacher import TeacherCreateRequest, TeacherListRequest
from .user import SetNameRequest, UserListRequest
from .schedule import ScheduleCreateRequest, ScheduleRequest
from .call import CallRequest

__all__ = [
    "StudentListRequest",
    "StudentCreateRequest",
    "TeacherListRequest",
    "TeacherCreateRequest",
    "UserListRequest",
    "SetNameRequest",
    "ScheduleCreateRequest",
    "ScheduleRequest",
    "CallRequest",
]