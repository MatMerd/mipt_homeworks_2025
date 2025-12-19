from fastapi import APIRouter, HTTPException, Query
from app.models.github import SearchParams
from app.services.github_service import GitHubService
from typing import Optional

router = APIRouter(prefix="/github", tags=["github"])

github_service = GitHubService()


@router.get("/search")
async def search_github_repositories(
    limit: int = Query(10, description="Количество репозиториев"),
    offset: int = Query(0, description="Смещение"),
    lang: str = Query(description="Язык программирования"),
    stars_min: int = Query(0, description="Минимальное количество звезд"),
    stars_max: Optional[int] = Query(None, description="Максимальное количество звезд"),
    forks_min: int = Query(0, description="Минимальное количество форков"),
    forks_max: Optional[int] = Query(
        None, description="Максимальное количество форков"
    ),
):
    """Поиск репозиториев GitHub и сохранение в CSV"""
    try:
        params = SearchParams(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )
        repositories = await github_service.search_repositories(params)
        if not repositories:
            raise HTTPException(
                status_code=404, detail="No repositories found matching the criteria"
            )
        filename = f"repositories_{params.lang}_{params.limit}_{params.offset}.csv"
        github_service.save_to_csv(repositories, filename)

        return {
            "message": "Search completed successfully",
            "filename": filename,
            "repositories_found": len(repositories),
            "download_url": f"/static/{filename}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
