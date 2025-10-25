import statistics
import json

class Stats:
    def __init__(self, data):
        self.data = data

    def median(self):
        sizes = [
            int(row["Size"])
            for row in self.data
            if row.get("Size")
        ]
        if not sizes:
            return None
        return statistics.median(sizes)

    def most_starred(self):
        starred = [
            row for row in self.data
            if row.get("Stars")
        ]
        if not starred:
            return None
        return max(starred, key=lambda x: int(x["Stars"]))

    def without_language(self):
        return [row for row in self.data
                if not row.get("Language") or row["Language"] == ""
        ]

    def top_committed(self, n=10):
        with_commits = [
            row for row in self.data
            if row.get("Commits")
        ]
        sorted_by_commits = sorted(with_commits, key=lambda x: int(x["Commits"]), reverse=True)
        return sorted_by_commits[:n]

    def collect_all(self):
        return {
            "median_repo_size": self.median(),
            "most_starred_repo": self.most_starred(),
            "repos_without_language": self.without_language(),
            "top_10_committed_repos": self.top_committed(10)
        }

    def save_json(self, filename):
        stats = self.collect_all()
        with open(filename, "w") as f:
            json.dump(stats, f)