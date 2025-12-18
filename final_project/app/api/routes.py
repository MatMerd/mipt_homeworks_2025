from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.infrastructure.http_client import github_client
from app.services.csv_service import generate_filename, write_csv
from app.services.github_service import build_search_query, fetch_repositories


router = APIRouter()
STATIC_DIR = Path(__file__).parent.parent.parent / "static"


@router.get("/search")
async def search_repositories(
    limit: int = Query(..., gt=0),
    lang: str = Query(...),
    offset: int = Query(..., ge=0),
    stars_min: int = Query(default=0, ge=0),
    stars_max: int | None = Query(default=None, ge=0),
    forks_min: int = Query(default=0, ge=0),
    forks_max: int | None = Query(default=None, ge=0),
) -> dict:
    try:
        query = build_search_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        repositories = await fetch_repositories(
            client=github_client,
            query=query,
            limit=limit,
            offset=offset,
        )

        filename = generate_filename(lang, limit, offset)
        filepath = STATIC_DIR / filename

        await write_csv(str(filepath), repositories)

        return {
            "status": "success",
            "filename": filename,
            "count": len(repositories),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
