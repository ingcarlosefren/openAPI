from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False,
)


class Base(DeclarativeBase):
	pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
	async with AsyncSessionLocal() as session:
		yield session


async def init_db() -> None:
	from src.modules.articles.infrastructure.persistence.sqlalchemy_article_model import (  # noqa: F401
		SQLAlchemyArticle,
	)
	from src.modules.users.infrastructure.persistence.sqlalchemy_user_model import (  # noqa: F401
		SQLAlchemyUser,
	)

	async with engine.begin() as connection:
		await connection.run_sync(Base.metadata.create_all)
