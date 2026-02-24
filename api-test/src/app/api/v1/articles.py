from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import Response
from pydantic import BaseModel
from pydantic import Field
from starlette.responses import JSONResponse

from src.app.api.errors import ResponseError
from src.app.api.errors import error_response
from src.app.api.dependencies import get_article_repository
from src.app.api.dependencies import get_user_repository
from src.modules.articles.application.create_article import CreateArticleUseCase
from src.modules.articles.application.get_article import GetArticleByIdUseCase
from src.modules.articles.application.get_article import GetArticlesByUserUseCase
from src.modules.articles.application.get_article import GetArticlesUseCase
from src.modules.articles.application.put_article import PutArticleUseCase
from src.modules.articles.domain.exceptions import ArticleNotFoundError
from src.modules.articles.domain.exceptions import AuthorNotFoundError
from src.modules.articles.domain.exceptions import InvalidArticleDataError
from src.modules.articles.domain.models.article import Article
from src.modules.articles.domain.models.article import ArticleCategory
from src.modules.articles.domain.repository import ArticleRepository
from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.application.get_user import GetUserByIdUseCase
from src.modules.users.domain.repository import UserRepository

router = APIRouter(tags=["Articles"])


class ArticlePost(BaseModel):
    title: str
    content: str
    author: UUID
    rating: float | None = Field(default=None, ge=0, le=5)
    category: ArticleCategory


class ArticleResponse(BaseModel):
    id: UUID
    created: int
    title: str
    content: str
    author: UUID
    rating: float | None = None
    category: ArticleCategory


class ArticlesResponse(BaseModel):
    data: list[ArticleResponse]


def _to_response(article: Article) -> ArticleResponse:
    return ArticleResponse(
        id=article.id,
        created=article.created,
        title=article.title,
        content=article.content,
        author=article.author,
        rating=article.rating,
        category=article.category,
    )


@router.get(
    "/articles",
    response_model=ArticlesResponse,
    operation_id="getArticles",
)
async def get_articles(
    category: ArticleCategory | None = Query(default=None),
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> ArticlesResponse:
    articles = await GetArticlesUseCase(article_repository).execute(category=category)
    return ArticlesResponse(data=[_to_response(article) for article in articles])


@router.post(
    "/articles",
    response_model=ArticleResponse,
    status_code=201,
    operation_id="createArticle",
    responses={400: {"model": ResponseError}},
)
async def create_article(
    payload: ArticlePost,
    response: Response,
    article_repository: ArticleRepository = Depends(get_article_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ArticleResponse | JSONResponse:
    try:
        article = await CreateArticleUseCase(article_repository, user_repository).execute(
            title=payload.title,
            content=payload.content,
            author=payload.author,
            category=payload.category,
            rating=payload.rating,
        )
    except (InvalidArticleDataError, AuthorNotFoundError) as error:
        return error_response(
            status_code=400,
            code="VALIDATION_ERROR",
            message=str(error),
        )

    response.headers["Location"] = f"/v1/articles/{article.id}"
    return _to_response(article)


@router.get(
    "/articles/{id}",
    response_model=ArticleResponse,
    operation_id="getArticleById",
    responses={404: {"model": ResponseError}},
)
async def get_article_by_id(
    id: UUID,
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> ArticleResponse | JSONResponse:
    try:
        article = await GetArticleByIdUseCase(article_repository).execute(id)
    except ArticleNotFoundError:
        return error_response(
            status_code=404,
            code="NOT_FOUND",
            message="The requested resource does not exist",
        )
    return _to_response(article)


@router.put(
    "/articles/{id}",
    response_model=ArticleResponse,
    operation_id="putArticle",
    responses={400: {"model": ResponseError}, 404: {"model": ResponseError}},
)
async def put_article(
    id: UUID,
    payload: ArticlePost,
    article_repository: ArticleRepository = Depends(get_article_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ArticleResponse | JSONResponse:
    try:
        article = await PutArticleUseCase(article_repository, user_repository).execute(
            id,
            title=payload.title,
            content=payload.content,
            author=payload.author,
            category=payload.category,
            rating=payload.rating,
        )
    except (InvalidArticleDataError, AuthorNotFoundError) as error:
        return error_response(
            status_code=400,
            code="VALIDATION_ERROR",
            message=str(error),
        )
    except ArticleNotFoundError:
        return error_response(
            status_code=404,
            code="NOT_FOUND",
            message="The requested resource does not exist",
        )
    return _to_response(article)


@router.get(
    "/users/{id}/articles",
    response_model=ArticlesResponse,
    operation_id="getArticlesByUser",
    tags=["Users", "Articles"],
)
async def get_articles_by_user(
    id: UUID,
    category: ArticleCategory | None = Query(default=None),
    article_repository: ArticleRepository = Depends(get_article_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ArticlesResponse | JSONResponse:
    try:
        await GetUserByIdUseCase(user_repository).execute(id)
    except UserNotFoundError:
        return error_response(
            status_code=404,
            code="NOT_FOUND",
            message="The requested resource does not exist",
        )

    articles = await GetArticlesByUserUseCase(article_repository).execute(
        id,
        category=category,
    )
    return ArticlesResponse(data=[_to_response(article) for article in articles])