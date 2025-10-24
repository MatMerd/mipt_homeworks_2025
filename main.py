from repositories.reader import CSVRepositoryReader
from repositories.models import Repository, SortOrder
from repositories.query_builder import RepositoryQueryBuilder
from repositories.statistics import RepositoryStatistics
from repositories.exporter import StatisticsExporter

if __name__ == '__main__':
    reader = CSVRepositoryReader('repositories.csv')
    repos = reader.read_from_file()
    query = RepositoryQueryBuilder(repos)
    top = query.filter(lambda r: r.stars > 5000).sort_by(lambda r: r.stars, SortOrder.DESCENDING).execute()
    stats = RepositoryStatistics(repos)
    report = stats.statistics_for_selection(top)
    StatisticsExporter.export_to_json(report, 'summary.json')
