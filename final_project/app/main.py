from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.settings import settings

app = FastAPI(
    title="GitHub Repository Search Service",
    description="Service for searching GitHub repositories and exporting to CSV",
    version="0.1.0",
)

app.include_router(api_router)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
