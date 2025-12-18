from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.routes import router
from app.infrastructure.http_client import github_client


STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    STATIC_DIR.mkdir(exist_ok=True)
    yield
    await github_client.close()


app = FastAPI(
    title="GitHub Repository Search",
    lifespan=lifespan,
)

app.include_router(router)
