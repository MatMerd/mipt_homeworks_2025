from fastapi import FastAPI, Query
from typing import Optional
from homework_final.services.repo_service import RepositoryService

app = FastAPI()
repo_service = RepositoryService()


@app.get("/api/repos")
async def get_repositories(
    limit: int = Query(10, description="Сколько репозиториев вернуть"),
    offset: int = Query(0, description="Смещение"),
    lang: str = Query(..., description="Язык программирования"),
    stars_min: int = Query(0, description="Мин. количество звезд"),
    stars_max: Optional[int] = Query(None, description="Макс. количество звезд"),
    forks_min: int = Query(0, description="Мин. количество форков"),
    forks_max: Optional[int] = Query(None, description="Макс. количество форков"),
):
    filepath = await repo_service.fetch_and_save_repos(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
    )

    return {
        "status": "success",
        "message": f"Found repositories and saved to {filepath}",
        "file_url": filepath,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8047)
