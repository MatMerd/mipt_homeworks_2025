from .db import Database
from .manager import DBManager

class DBConnect:
    def __init__(self, file_path):
        self.base = DBManager.openDBConnect(file_path)
        self.file_path = file_path
        self.queries = []
        self.closed = False
    
    def get_headers(self):
        return self.base.header
    
    def add_query(self, query):
        self.queries.append(query)
    
    def clear(self):
        self.queries.clear()

    def execute(self):
        self.base.execute(self.queries)
        self.queries.clear()

    def close(self):
        if not self.closed:
            self.closed = True
            DBManager.closeDBConnect(self.file_path)
        else:
            raise Exception("The connection is already closed")

    def __del__(self):
        if not self.closed:
            self.close()