from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from uuid import UUID


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    PREMIUM = "PREMIUM"
    FREE = "FREE"


@dataclass(slots=True)
class User:
    id: UUID
    name: str
    email: str
    birth_date: date
    role: UserRole = UserRole.FREE


@dataclass(slots=True)
class UserPatchData:
    name: str | None = None
    email: str | None = None
    birth_date: date | None = None