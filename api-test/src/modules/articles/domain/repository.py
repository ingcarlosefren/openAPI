from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory


class ArticleRepository(ABC):
    @abstractmethod
    async def create(
        self,
        *,
        title: str,
        content: str,
        author: UUID,
        category: ArticleCategory,
        rating: float | None,
    ) -> Article:
        raise NotImplementedError

    @abstractmethod
    async def list(self, *, category: ArticleCategory | None = None) -> list[Article]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, article_id: UUID) -> Article | None:
        raise NotImplementedError

    @abstractmethod
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

    @abstractmethod
    async def list_by_user(
        self,
        user_id: UUID,
        *,
        category: ArticleCategory | None = None,
    ) -> list[Article]:
        raise NotImplementedError