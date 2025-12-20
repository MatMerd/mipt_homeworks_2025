from fastapi.routing import APIRouter

from final_project.web.api import github_repositories, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(github_repositories.router)
