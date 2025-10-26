import statistics
from typing import List, Dict, Any, Tuple, cast
from homework_oop.repository import Repository
from homework_oop.queries import Projection


class Statistics:
    def __init__(self, data: List[Repository]):
        self.data = data

    def median_size(self) -> float:
        projection = cast(
            List[Dict[str, Any]],
            Projection(self.data).select("Size").execute(),
        )

        sizes = [repo["Size"] for repo in projection]
        return statistics.median(sizes)

    def max_stars(self) -> int:
        projection = cast(
            List[Dict[str, Any]],
            Projection(self.data).select("Stars").execute(),
        )
        stars = [repo["Stars"] for repo in projection]
        return max(stars)

    def repos_without_language(self) -> int:
        projection = cast(
            List[Dict[str, Any]],
            Projection(self.data).select("Language").execute(),
        )
        return sum(
            (repo["Language"] == "" or repo["Language"] is None) for repo in projection
        )

    def top_10_forks(self) -> List[Dict[str, Any]]:
        projection = cast(
            List[Dict[str, Any]],
            Projection(self.data)
            .select("Name", "Forks")
            .sort_by("Forks", reverse=True)
            .execute(),
        )
        return projection[:10]

    def top_10_popular_languages(self) -> List[Dict[str, Any]]:
        projection = cast(
            Dict[Tuple[Any, ...], List[Dict[str, Any]]],
            Projection(self.data)
            .filter(lambda repo: repo.language is not None and repo.language != "")
            .select("Language")
            .group_by("Language")
            .execute(),
        )

        result: Dict[str, int] = {}
        for lang, repos in projection.items():
            key = lang[0]
            result[key] = sum(1 for _ in repos)

        sorted_langs = sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]

        return [
            {"Language": lang, "Number of repos": number}
            for lang, number in sorted_langs
        ]
