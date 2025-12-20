from fastapi import APIRouter

from .views import router as views_router

router = APIRouter(prefix="/github-repos", tags=["github-repos"])
router.include_router(views_router)
