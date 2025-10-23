from .db import Database
from .db_manager import DBManager

class DBConnect:
    def __init__(self, file_path):
        self.base = DBManager.openDBConnect(file_path)
        self.queries = []
    
    def get_headers(self):
        return self.base.header
    
    def add_query(self, query):
        self.queries.append(query)
    
    def clear(self):
        self.queries.clear()

    def execute(self):
        self.base.execute(self.queries)
        self.queries.clear()