from fastapi import APIRouter, HTTPException, Query

from app.models import SearchParams, SearchResponse
from app.services.repository_service import repository_service

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.get("/search", response_model=SearchResponse)
async def search_repositories(
    limit: int = Query(..., ge=1, le=1000),
    offset: int = Query(0, ge=0),
    lang: str = Query(...),
    stars_min: int = Query(0, ge=0),
    stars_max: int | None = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: int | None = Query(None, ge=0),
) -> SearchResponse:
    params = SearchParams(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
    )

    try:
        result = await repository_service.search_and_save(params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
