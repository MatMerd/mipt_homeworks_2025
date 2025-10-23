class StatisticsCalc:
    def __init__(self, data):
        if data and isinstance(data[0], list):
            headers = data[0]
            self.data = []
            for row in data[1:]:
                item_dict = {}
                for i, header in enumerate(headers):
                    item_dict[header] = row[i]
                self.data.append(item_dict)
        else:
            self.data = data

    def median_by_size_repository(self):
        if not self.data:
            return None

        sizes = []
        for repo in self.data:
            try:
                sizes.append(int(repo.get("Size", 0)))
            except (ValueError, TypeError):
                sizes.append(0)

        if not sizes:
            return None

        sorted_sizes = sorted(sizes)
        n = len(sorted_sizes)
        middle = n // 2

        if n % 2 == 0:
            return (sorted_sizes[middle - 1] + sorted_sizes[middle]) / 2
        else:
            return sorted_sizes[middle]

    def most_starred_repo(self):
        if not self.data:
            return None

        max_stars = -1
        max_repo = None

        for repo in self.data:
            try:
                stars = int(repo.get("Stars", 0))
                if stars > max_stars:
                    max_stars = stars
                    max_repo = repo
            except (ValueError, TypeError):
                continue

        return max_repo

    def repos_without_language(self):
        return [repo for repo in self.data if not repo.get("Language", "").strip()]

    def top_forks_repos(self, top_n=10):
        repos_with_forks = []
        for repo in self.data:
            try:
                forks = int(repo.get("Forks", 0))
                repos_with_forks.append((repo, forks))
            except (ValueError, TypeError):
                repos_with_forks.append((repo, 0))

        repos_with_forks.sort(key=lambda x: x[1], reverse=True)

        return [repo for repo, forks in repos_with_forks[:top_n]]

    def total_forks(self):
        total = 0
        for repo in self.data:
            try:
                total += int(repo.get("Forks", 0))
            except (ValueError, TypeError):
                continue
        return total
