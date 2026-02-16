
from rodi import Container

from repositories import UserRepository, StudentRepository, TeacherRepository
from services import WeatherService, StudentService
from services.teacher import TeacherService

container = Container()


def setup_dependencies() -> None:

    # repo
    container.add_transient(UserRepository)
    container.add_transient(StudentRepository)
    container.add_transient(TeacherRepository)

    # service
    container.add_scoped(WeatherService)
    container.add_scoped(StudentService)
    container.add_scoped(TeacherService)

def get_user_repository() -> UserRepository:
    return container.resolve(UserRepository)

def get_weather_service() -> WeatherService:
    return container.resolve(WeatherService)

def get_student_service() -> StudentService:
    return container.resolve(StudentService)

def get_teacher_service() -> TeacherService:
    return container.resolve(TeacherService)