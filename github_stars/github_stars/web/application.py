from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from github_stars.web.api.router import api_router
from github_stars.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="github_stars",
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    @app.get("/")
    def root() -> dict[str, bool]:
        return {"ok": True}

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
