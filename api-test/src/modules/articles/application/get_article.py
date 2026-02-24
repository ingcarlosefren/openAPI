from uuid import UUID

from src.modules.articles.domain.exceptions import ArticleNotFoundError
from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory
from src.modules.articles.domain.repository import ArticleRepository


class GetArticlesUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, *, category: ArticleCategory | None = None) -> list[Article]:
        return await self._repository.list(category=category)


class GetArticleByIdUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, article_id: UUID) -> Article:
        article = await self._repository.get_by_id(article_id)
        if article is None:
            raise ArticleNotFoundError("Article not found")
        return article


class GetArticlesByUserUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        user_id: UUID,
        *,
        category: ArticleCategory | None = None,
    ) -> list[Article]:
        return await self._repository.list_by_user(user_id, category=category)