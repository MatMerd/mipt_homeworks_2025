from .csvloader import CSVLoader
from .indexer import Indexer
from .queryexecutor import QueryExecutor

class Database:
    def __init__(self, filename, delimiter=',', auto_typization=True, index_fields=()):
        self.loader = CSVLoader(filename, delimiter, auto_typization)
        self.loader.load()
        self.indexer = Indexer(self.loader.rows, self.loader.header, index_fields)
        self.indexer.create_indexes()
        self.query_engine = QueryExecutor(
            header=self.loader.header,
            field_idx=self.loader.field_idx,
            indexer=self.indexer
        )

    def execute(self, queries):
        return self.query_engine.execute(self.loader.rows, queries)