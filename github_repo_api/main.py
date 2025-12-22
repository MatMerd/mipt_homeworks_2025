from fastapi import FastAPI

from github_repo_api.web.application import get_app


def get_instance() -> FastAPI:
    """
    Get FastAPI instance.

    :return: FastAPI application instance
    """
    return get_app()
