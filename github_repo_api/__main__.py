import uvicorn
from settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "github_repo_api.main:get_instance",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
