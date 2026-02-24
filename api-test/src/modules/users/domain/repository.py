from abc import ABC
from abc import abstractmethod
from datetime import date
from uuid import UUID

from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserPatchData


class UserRepository(ABC):
    @abstractmethod
    async def create(self, *, name: str, email: str, birth_date: date) -> User:
        raise NotImplementedError

    @abstractmethod
    async def list(self, *, filter_by_name: str | None = None) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update_partial(self, user_id: UUID, patch: UserPatchData) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        raise NotImplementedError