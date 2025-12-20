from fastapi.routing import APIRouter

from github_stars.web.api import monitoring
from github_stars.web.api.github_repos.router import router as github_repos_router

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(github_repos_router)
