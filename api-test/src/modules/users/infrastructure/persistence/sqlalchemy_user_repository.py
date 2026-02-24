from datetime import date
from uuid import UUID
from uuid import uuid4

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.domain.exceptions import DuplicateUserEmailError
from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserPatchData
from src.modules.users.domain.repository import UserRepository
from src.modules.users.infrastructure.mappers.user_mapper import to_domain
from src.modules.users.infrastructure.persistence.sqlalchemy_user_model import (
    SQLAlchemyUser,
)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, *, name: str, email: str, birth_date: date) -> User:
        user_model = SQLAlchemyUser(
            id=str(uuid4()),
            name=name,
            email=email,
            birth_date=birth_date,
            role="FREE",
        )
        self._session.add(user_model)
        try:
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise DuplicateUserEmailError("Email already exists") from error
        await self._session.refresh(user_model)
        return to_domain(user_model)

    async def list(self, *, filter_by_name: str | None = None) -> list[User]:
        statement = select(SQLAlchemyUser)
        if filter_by_name:
            statement = statement.where(SQLAlchemyUser.name.ilike(f"%{filter_by_name}%"))
        result = await self._session.execute(statement)
        return [to_domain(user) for user in result.scalars().all()]

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(
            select(SQLAlchemyUser).where(SQLAlchemyUser.id == str(user_id))
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return None
        return to_domain(user_model)

    async def update_partial(self, user_id: UUID, patch: UserPatchData) -> User | None:
        result = await self._session.execute(
            select(SQLAlchemyUser).where(SQLAlchemyUser.id == str(user_id))
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return None

        if patch.name is not None:
            user_model.name = patch.name
        if patch.email is not None:
            user_model.email = patch.email
        if patch.birth_date is not None:
            user_model.birth_date = patch.birth_date

        try:
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise DuplicateUserEmailError("Email already exists") from error
        await self._session.refresh(user_model)
        return to_domain(user_model)

    async def delete(self, user_id: UUID) -> bool:
        result = await self._session.execute(
            delete(SQLAlchemyUser)
            .where(SQLAlchemyUser.id == str(user_id))
            .returning(SQLAlchemyUser.id)
        )
        deleted_id = result.scalar_one_or_none()
        await self._session.commit()
        return deleted_id is not None