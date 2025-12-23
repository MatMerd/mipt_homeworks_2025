from typing import Iterable, Iterator, Any
import logging

logger = logging.getLogger("batching")


def batch_repositories(
        repositories: Iterable[dict[str, Any]],
        batch_size: int = 1000,
) -> Iterator[list[dict[str, Any]]]:
    batch: list[dict[str, Any]] = []

    for repo in repositories:
        batch.append(repo)

        if len(batch) == batch_size:
            logger.debug(f"Yielding batch of {len(batch)} repositories")
            yield batch
            batch = []
    if batch:
        logger.debug(f"Yielding final batch of {len(batch)} repositories")
        yield batch