from dataclasses import dataclass
from datetime import date
from uuid import UUID
from uuid import uuid4

import pytest

from src.modules.users.application.update_user import UpdateUserUseCase
from src.modules.users.domain.exceptions import InvalidUserPatchError
from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserPatchData
from src.modules.users.domain.models.user import UserRole


@dataclass
class FakeUserRepository:
    existing_user: User | None = None

    async def create(self, *, name: str, email: str, birth_date: date) -> User:
        raise NotImplementedError

    async def list(self, *, filter_by_name: str | None = None) -> list[User]:
        raise NotImplementedError

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.existing_user

    async def update_partial(self, user_id: UUID, patch: UserPatchData) -> User | None:
        if self.existing_user is None:
            return None
        if patch.name is not None:
            self.existing_user.name = patch.name
        if patch.email is not None:
            self.existing_user.email = patch.email
        if patch.birth_date is not None:
            self.existing_user.birth_date = patch.birth_date
        return self.existing_user

    async def delete(self, user_id: UUID) -> bool:
        raise NotImplementedError


@pytest.mark.asyncio
async def test_update_user_fails_when_patch_is_empty() -> None:
    repository = FakeUserRepository(
        existing_user=User(
            id=uuid4(),
            name="Ana",
            email="ana@example.com",
            birth_date=date(1990, 1, 1),
            role=UserRole.FREE,
        )
    )

    use_case = UpdateUserUseCase(repository)

    with pytest.raises(InvalidUserPatchError):
        await use_case.execute(repository.existing_user.id, UserPatchData())


@pytest.mark.asyncio
async def test_update_user_fails_when_user_not_found() -> None:
    repository = FakeUserRepository(existing_user=None)
    use_case = UpdateUserUseCase(repository)

    with pytest.raises(UserNotFoundError):
        await use_case.execute(uuid4(), UserPatchData(name="Nuevo"))
