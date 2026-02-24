from __future__ import annotations

from datetime import datetime
from datetime import timezone
from uuid import UUID
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory
from src.modules.articles.domain.repository import ArticleRepository
from src.modules.articles.infrastructure.mappers.article_mapper import to_domain
from src.modules.articles.infrastructure.persistence.sqlalchemy_article_model import (
    SQLAlchemyArticle,
)


def _epoch_ms_now() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


class SQLAlchemyArticleRepository(ArticleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        title: str,
        content: str,
        author: UUID,
        category: ArticleCategory,
        rating: float | None,
    ) -> Article:
        article_model = SQLAlchemyArticle(
            id=str(uuid4()),
            created=_epoch_ms_now(),
            title=title,
            content=content,
            author=str(author),
            category=category.value,
            rating=rating,
        )
        self._session.add(article_model)
        await self._session.commit()
        await self._session.refresh(article_model)
        return to_domain(article_model)

    async def list(self, *, category: ArticleCategory | None = None) -> list[Article]:
        statement = select(SQLAlchemyArticle)
        if category is not None:
            statement = statement.where(SQLAlchemyArticle.category == category.value)
        result = await self._session.execute(statement)
        return [to_domain(article) for article in result.scalars().all()]

    async def get_by_id(self, article_id: UUID) -> Article | None:
        result = await self._session.execute(
            select(SQLAlchemyArticle).where(SQLAlchemyArticle.id == str(article_id))
        )
        article_model = result.scalar_one_or_none()
        if article_model is None:
            return None
        return to_domain(article_model)

    async def replace(
        self,
        article_id: UUID,
        *,
        title: str,
        content: str,
        author: UUID,
        category: ArticleCategory,
        rating: float | None,
    ) -> Article | None:
        result = await self._session.execute(
            select(SQLAlchemyArticle).where(SQLAlchemyArticle.id == str(article_id))
        )
        article_model = result.scalar_one_or_none()
        if article_model is None:
            return None

        article_model.title = title
        article_model.content = content
        article_model.author = str(author)
        article_model.category = category.value
        article_model.rating = rating

        await self._session.commit()
        await self._session.refresh(article_model)
        return to_domain(article_model)

    async def list_by_user(
        self,
        user_id: UUID,
        *,
        category: ArticleCategory | None = None,
    ) -> list[Article]:
        statement = select(SQLAlchemyArticle).where(SQLAlchemyArticle.author == str(user_id))
        if category is not None:
            statement = statement.where(SQLAlchemyArticle.category == category.value)
        result = await self._session.execute(statement)
        return [to_domain(article) for article in result.scalars().all()]