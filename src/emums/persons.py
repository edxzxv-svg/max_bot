from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    GUEST = 'quest'

class UserStatus(StrEnum):
    ACTIVE = 'active'
    BANNED = 'banned'

