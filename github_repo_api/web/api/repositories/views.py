from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from github_repo_api.services.repository_service import RepositoryService

router = APIRouter()


@router.post("/search")
async def search_repositories(
    limit: int = Query(
        ..., ge=1, le=100, description="Количество репози   ториев для поиска (1-100)"
    ),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    lang: str = Query(None, description="Язык программирования репозитория"),
    stars_min: int = Query(0, ge=0, description="Минимальное количество звезд"),
    stars_max: int = Query(None, ge=0, description="Максимальное количество звезд"),
    forks_min: int = Query(0, ge=0, description="Минимальное количество форков"),
    forks_max: int = Query(None, ge=0, description="Максимальное количество форков"),
) -> JSONResponse:
    """
    Поиск GitHub репозиториев и сохранение результатов в CSV файл.

    :param limit: Количество репозиториев для поиска
    :param offset: Смещение для пагинации
    :param lang: Язык программирования
    :param stars_min: Минимальное количество звезд
    :param stars_max: Максимальное количество звезд
    :param forks_min: Минимальное количество форков
    :param forks_max: Максимальное количество форков
    :return: Путь к созданному CSV файлу
    """
    try:
        service = RepositoryService()

        csv_filename = await service.search_and_save_repositories(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
        )

        return JSONResponse(
            content={
                "message": "Репозитории успешно найдены и сохранены",
                "csv_file": csv_filename,
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None
    except RuntimeError as e:
        if "rate limit" in str(e):
            raise HTTPException(status_code=429, detail=str(e)) from None
        raise HTTPException(status_code=500, detail=str(e)) from None
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e!s}"
        ) from None
