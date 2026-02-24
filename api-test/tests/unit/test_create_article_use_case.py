from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID
from uuid import uuid4

import pytest

from src.modules.articles.application.create_article import CreateArticleUseCase
from src.modules.articles.domain.exceptions import AuthorNotFoundError
from src.modules.articles.domain.exceptions import InvalidArticleDataError
from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory
from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserRole


@dataclass
class FakeArticleRepository:
    async def create(
        self,
        *,
        title: str,
        content: str,
        author: UUID,
        category: ArticleCategory,
        rating: float | None,
    ) -> Article:
        return Article(
            id=uuid4(),
            created=1708700000000,
            title=title,
            content=content,
            author=author,
            category=category,
            rating=rating,
        )

    async def list(self, *, category: ArticleCategory | None = None) -> list[Article]:
        raise NotImplementedError

    async def get_by_id(self, article_id: UUID) -> Article | None:
        raise NotImplementedError

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
        raise NotImplementedError

    async def list_by_user(
        self,
        user_id: UUID,
        *,
        category: ArticleCategory | None = None,
    ) -> list[Article]:
        raise NotImplementedError


@dataclass
class FakeUserRepository:
    user_exists: bool

    async def create(self, *, name: str, email: str, birth_date):  # pragma: no cover
        raise NotImplementedError

    async def list(self, *, filter_by_name: str | None = None):  # pragma: no cover
        raise NotImplementedError

    async def get_by_id(self, user_id: UUID) -> User | None:
        if not self.user_exists:
            return None
        return User(
            id=user_id,
            name="Ana",
            email="ana@example.com",
            birth_date=date(1990, 1, 1),
            role=UserRole.FREE,
        )

    async def update_partial(self, user_id: UUID, patch):  # pragma: no cover
        raise NotImplementedError

    async def delete(self, user_id: UUID):  # pragma: no cover
        raise NotImplementedError


@pytest.mark.asyncio
async def test_create_article_fails_when_author_not_found() -> None:
    use_case = CreateArticleUseCase(
        article_repository=FakeArticleRepository(),
        user_repository=FakeUserRepository(user_exists=False),
    )

    with pytest.raises(AuthorNotFoundError):
        await use_case.execute(
            title="Articulo",
            content="Contenido",
            author=uuid4(),
            category=ArticleCategory.AI,
            rating=4.0,
        )


@pytest.mark.asyncio
async def test_create_article_fails_when_rating_is_out_of_range() -> None:
    use_case = CreateArticleUseCase(
        article_repository=FakeArticleRepository(),
        user_repository=FakeUserRepository(user_exists=True),
    )

    with pytest.raises(InvalidArticleDataError):
        await use_case.execute(
            title="Articulo",
            content="Contenido",
            author=uuid4(),
            category=ArticleCategory.AI,
            rating=9.0,
        )
