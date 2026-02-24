from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class ArticleCategory(StrEnum):
    PROGRAMMING = "PROGRAMMING"
    AI = "AI"
    DATA = "DATA"
    BLOCKCHAIN = "BLOCKCHAIN"
    TESTING = "TESTING"


@dataclass(slots=True)
class Article:
    id: UUID
    created: int
    title: str
    content: str
    author: UUID
    category: ArticleCategory
    rating: float | None = None