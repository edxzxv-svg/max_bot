from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    GUEST = "guest"


class UserStatus(StrEnum):
    ACTIVE = "active"
    BANNED = "banned"
