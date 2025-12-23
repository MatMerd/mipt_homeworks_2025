from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..dependencies import get_repository_service
from ..schemas import SearchRepositoriesRequest
from ..services import RepositoryService

router = APIRouter()


@router.get("/search")
async def search_repositories(
    request: SearchRepositoriesRequest,
    service: RepositoryService = Depends(get_repository_service),
):
    try:
        filepath, count = await service.search_and_export_to_csv(request)
        return JSONResponse(
            content={
                "status": "success",
                "message": "Repositories exported to CSV",
                "file": filepath,
                "count": count,
                "filters": request.model_dump(),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
