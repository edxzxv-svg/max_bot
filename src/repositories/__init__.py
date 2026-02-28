from .user import UserRepository
from .student import StudentRepository
from .teacher import TeacherRepository
from .schedule import ScheduleRepository
from .call import CallRepository

__all__ = [
    'UserRepository',
    'StudentRepository',
    'TeacherRepository',
    'ScheduleRepository',
]