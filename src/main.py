from fastapi import FastAPI

from src.api.router import router

app = FastAPI(
    title="GitHub Search API",
    description="API for searching GitHub repositories and saving to CSV",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1", tags=["search"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
