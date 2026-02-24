from uuid import UUID

from src.modules.articles.domain.exceptions import AuthorNotFoundError
from src.modules.articles.domain.exceptions import InvalidArticleDataError
from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory
from src.modules.articles.domain.repository import ArticleRepository
from src.modules.users.domain.repository import UserRepository


class CreateArticleUseCase:
    def __init__(
        self,
        article_repository: ArticleRepository,
        user_repository: UserRepository,
    ) -> None:
        self._article_repository = article_repository
        self._user_repository = user_repository

    async def execute(
        self,
        *,
        title: str,
        content: str,
        author: UUID,
        category: ArticleCategory,
        rating: float | None,
    ) -> Article:
        if not title.strip() or not content.strip():
            raise InvalidArticleDataError("Title and content are required")

        if rating is not None and (rating < 0 or rating > 5):
            raise InvalidArticleDataError("Rating must be between 0 and 5")

        author_exists = await self._user_repository.get_by_id(author)
        if author_exists is None:
            raise AuthorNotFoundError("Author does not exist")

        return await self._article_repository.create(
            title=title,
            content=content,
            author=author,
            category=category,
            rating=rating,
        )