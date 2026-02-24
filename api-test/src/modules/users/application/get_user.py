from uuid import UUID

from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.models.user import User
from src.modules.users.domain.repository import UserRepository


class GetUsersUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, *, filter_by_name: str | None = None) -> list[User]:
        return await self._repository.list(filter_by_name=filter_by_name)


class GetUserByIdUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UUID) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        return user