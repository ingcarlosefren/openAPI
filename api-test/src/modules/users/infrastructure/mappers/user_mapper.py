from uuid import UUID

from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserRole
from src.modules.users.infrastructure.persistence.sqlalchemy_user_model import (
    SQLAlchemyUser,
)


def to_domain(model: SQLAlchemyUser) -> User:
    return User(
        id=UUID(model.id),
        name=model.name,
        email=model.email,
        birth_date=model.birth_date,
        role=UserRole(model.role),
    )