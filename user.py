from statistic import Statistic


class User:
    def __init__(self, name):
        self.name = name
        self.statistic = Statistic()
        self.requests = []

    def process_request(self, request):
        self.requests.append(request)
        # sorting, grouping, choosing...
        repos = [[], [], []]
        stats = []
        for group in repos:
            stat = self.statistic.get_all_statistics(group)
            stats.append(stat)

        return stats
