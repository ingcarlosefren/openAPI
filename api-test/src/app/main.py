from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.api.v1.articles import router as articles_router
from src.app.api.v1.health import router as health_router
from src.app.api.v1.users import router as users_router
from src.shared.infrastructure.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Users & Articles Management API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router, prefix="/v1")
app.include_router(users_router, prefix="/v1")
app.include_router(articles_router, prefix="/v1")