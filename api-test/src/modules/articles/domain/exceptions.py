class ArticleError(Exception):
    pass


class ArticleNotFoundError(ArticleError):
    pass


class InvalidArticleDataError(ArticleError):
    pass


class AuthorNotFoundError(ArticleError):
    pass