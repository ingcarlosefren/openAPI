from uuid import UUID

from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory
from src.modules.articles.infrastructure.persistence.sqlalchemy_article_model import (
    SQLAlchemyArticle,
)


def to_domain(model: SQLAlchemyArticle) -> Article:
    return Article(
        id=UUID(model.id),
        created=model.created,
        title=model.title,
        content=model.content,
        author=UUID(model.author),
        category=ArticleCategory(model.category),
        rating=model.rating,
    )