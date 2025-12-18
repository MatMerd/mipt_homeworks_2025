from fastapi import FastAPI

from src.api.repositories import router as repositories_router

app = FastAPI(
    title="GitHub Repository Search API",
    description="API для поиска GitHub репозиториев и сохранения в CSV",
    version="1.0.0",
)

app.include_router(repositories_router, prefix="/api")


@app.get("/")
async def root() -> dict:
    return {
        "message": "GitHub Repository Search API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy"}
