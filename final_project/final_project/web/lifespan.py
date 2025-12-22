from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from final_project.final_project.infrastructure.github_client import GitHubClient
from final_project.final_project.settings import settings


@asynccontextmanager
async def lifespan_setup(
        app: FastAPI,
) -> AsyncGenerator[None]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    headers = {}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    client = httpx.AsyncClient(headers=headers)

    app.state.github_client = GitHubClient(client=client, base_url=settings.GITHUB_BASE_URL)

    app.middleware_stack = None
    app.middleware_stack = app.build_middleware_stack()

    yield

    await client.aclose()
