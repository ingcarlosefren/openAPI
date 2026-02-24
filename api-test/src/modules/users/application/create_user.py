from datetime import date

from src.modules.users.domain.models.user import User
from src.modules.users.domain.repository import UserRepository


class CreateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, *, name: str, email: str, birth_date: date) -> User:
        return await self._repository.create(
            name=name,
            email=email,
            birth_date=birth_date,
        )