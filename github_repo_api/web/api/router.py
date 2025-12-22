from fastapi.routing import APIRouter

from github_repo_api.web.api import docs, monitoring, repositories

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(repositories.router)
