from fastapi import FastAPI
from app.api.endpoints import github
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(github.router, prefix=settings.API_V1_STR)


async def root():
    return {"message": "GitHub Search API"}
