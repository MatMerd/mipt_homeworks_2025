from fastapi import APIRouter, HTTPException, Query

from src.infrastructure.github_client import GitHubClient
from src.services.repository_service import RepositorySearchService

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.get("/search")
async def search_repositories(
    limit: int = Query(..., ge=1, le=1000, description="Количество репозиториев"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    lang: str = Query(..., description="Язык программирования"),
    stars_min: int = Query(0, ge=0, description="Минимальное количество звёзд"),
    stars_max: int | None = Query(None, ge=0, description="Максимальное количество звёзд"),
    forks_min: int = Query(0, ge=0, description="Минимальное количество форков"),
    forks_max: int | None = Query(None, ge=0, description="Максимальное количество форков"),
) -> dict:
    try:
        github_client = GitHubClient()
        service = RepositorySearchService(github_client)

        filepath = await service.search_and_save(
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
            "message": "Репозитории успешно сохранены",
            "filepath": filepath,
            "params": {
                "limit": limit,
                "offset": offset,
                "lang": lang,
                "stars_min": stars_min,
                "stars_max": stars_max,
                "forks_min": forks_min,
                "forks_max": forks_max,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
