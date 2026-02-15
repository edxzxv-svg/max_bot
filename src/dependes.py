
from rodi import Container

from repositories import UserRepository, StudentRepository
from services import WeatherService, StudentService

container = Container()


def setup_dependencies() -> None:

    # repo
    container.add_transient(UserRepository)
    container.add_transient(StudentRepository)


    # service
    container.add_scoped(WeatherService)
    container.add_scoped(StudentService)

def get_user_repository() -> UserRepository:
    return container.resolve(UserRepository)

def get_weather_service() -> WeatherService:
    return container.resolve(WeatherService)


def get_student_service() -> StudentService:
    return container.resolve(StudentService)
