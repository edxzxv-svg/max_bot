from src.models import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)
