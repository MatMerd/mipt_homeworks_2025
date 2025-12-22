from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI

import github_stars
from github_stars.infrastructure.github_client import GitHubClient
from github_stars.services.github_repos.service import (
    GitHubReposExportService,
    CsvWriterService,
)
from github_stars.services.redis.lifespan import init_redis, shutdown_redis


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

    app.middleware_stack = None
    init_redis(app)
    app.middleware_stack = app.build_middleware_stack()

    token = os.getenv("GITHUB_TOKEN")

    static_dir = Path(github_stars.__file__).resolve().parent / "static"
    static_dir.mkdir(parents=True, exist_ok=True)

    http = httpx.AsyncClient(timeout=30.0)
    github = GitHubClient(http=http, token=token)

    csv_writer = CsvWriterService()

    app.state.github_repos_export_service = GitHubReposExportService(
        github_client=github,
        csv_writer=csv_writer,
        static_dir=static_dir,
    )
    app.state.github_http_client = http

    try:
        yield
    finally:
        await app.state.github_http_client.aclose()

        await shutdown_redis(app)
