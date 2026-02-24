from uuid import UUID

from src.modules.users.domain.exceptions import InvalidUserPatchError
from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserPatchData
from src.modules.users.domain.repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UUID, patch: UserPatchData) -> User:
        if not any([patch.name, patch.email, patch.birth_date]):
            raise InvalidUserPatchError("At least one field must be provided")

        user = await self._repository.update_partial(user_id, patch)
        if user is None:
            raise UserNotFoundError("User not found")
        return user