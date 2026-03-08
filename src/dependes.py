
from rodi import Container

from src.repositories import (
    CallRepository,
    ScheduleRepository,
    StudentRepository,
    TeacherRepository,
    UserRepository,
)
from src.services import (
    CallService,
    ScheduleService,
    StudentService,
    TeacherService,
    WeatherService,
)

container = Container()


def setup_dependencies() -> None:

    # repo
    container.add_transient(UserRepository)
    container.add_transient(StudentRepository)
    container.add_transient(TeacherRepository)
    container.add_transient(ScheduleRepository)
    container.add_transient(CallRepository)

    # service
    container.add_scoped(WeatherService)
    container.add_scoped(StudentService)
    container.add_scoped(TeacherService)
    container.add_scoped(ScheduleService)
    container.add_scoped(CallService)

def get_user_repository() -> UserRepository:
    return container.resolve(UserRepository)

def get_student_repository() -> StudentRepository:
    return container.resolve(StudentRepository)

def get_teacher_repository() -> TeacherRepository:
    return container.resolve(TeacherRepository)

def get_weather_service() -> WeatherService:
    return container.resolve(WeatherService)

def get_student_service() -> StudentService:
    return container.resolve(StudentService)

def get_teacher_service() -> TeacherService:
    return container.resolve(TeacherService)

def get_schedule_service() -> ScheduleService:
    return container.resolve(ScheduleService)

def get_call_service() -> CallService:
    return container.resolve(CallService)
