from uuid import UUID

from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.repository import UserRepository


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UUID) -> None:
        deleted = await self._repository.delete(user_id)
        if not deleted:
            raise UserNotFoundError("User not found")