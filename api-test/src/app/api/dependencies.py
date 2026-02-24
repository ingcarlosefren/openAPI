from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.articles.domain.repository import ArticleRepository
from src.modules.articles.infrastructure.persistence.sqlalchemy_article_repository import (
    SQLAlchemyArticleRepository,
)
from src.modules.users.domain.repository import UserRepository
from src.modules.users.infrastructure.persistence.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from src.shared.infrastructure.database import get_db_session


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[UserRepository, None]:
    yield SQLAlchemyUserRepository(session)


async def get_article_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ArticleRepository, None]:
    yield SQLAlchemyArticleRepository(session)