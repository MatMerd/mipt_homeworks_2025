import csv
import os
import datetime

class Database:
    def __init__(self, filename, delimiter=',', auto_typization=True, auto_indexing=True, index_fields=()):
        self.filename = filename
        if not os.path.exists(self.filename):
            raise Exception(f"Database file {self.filename} not found.")

        self.header = []
        self.rows = []
        self.indexes = dict()

        self.auto_typization = auto_typization
        self.auto_indexing = auto_indexing
        self.index_fields = index_fields
        
        if self.auto_indexing:
            self.index_fields = [self.header[0]]
        
        self._load_data(delimiter)
        self._create_indexes()
    
    def _auto_type(self, value):
        if not self.auto_typization:
            return value

        for cast in (int, float, bool):
            try:
                return cast(value)
            except ValueError:
                continue
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            return value

    def _load_data(self, delimiter):
        try:
            file = open(self.filename, 'r', encoding='utf-8')
            reader = csv.DictReader(file, delimiter=delimiter)

            self.header = reader.fieldnames
            self.rows = [(self._auto_type(i) for i in row) for row in reader]
            file.close()
        except Exception as e:
            raise Exception(f"Error reading database file: {e}")
    
    def _create_indexes(self):
        for field in self.index_fields:
            self.indexes[field] = dict()
            for row in self.rows:
                key = row[self.header.index(field)]
                if key not in self.indexes[field].keys():
                    self.indexes[field][key] = []
                self.indexes[field][key].append(row)    

    def _sort_queries(self, queries):
        where = []
        wherelen = []
        sort = []
        group = []

        last_prior = -1
        for query in queries:
            type = query[0]
            if type == 'WHERE':
                spec = query[1]
                field = query[2]
                value = query[3]
                if spec == '==' and field in self.index_fields:
                    prior = self.indexes[field][value]
                    if last_prior == -1 or last_prior > prior:
                        where.insert(0, query)
                        last_prior = prior
                    else:
                        where.append(query)
                else:
                    where.append(query)
            elif type == 'WHERELEN':
                wherelen.append(query)
            elif type == 'SORT':
                sort.append(query)
            elif type == 'GROUP':
                group.append(query)
        
        queries = where + wherelen + sort + group

    def _where(self, query, results):
        type = query[1]
        field = query[2]
        value = query[3]
        value2 = query[4] if type == 'btw' else None

        if type == '==' and field in self.indexes and len(results) == 0:
            results = self.indexes[field].get(value, [])
        elif type == '==':
            results = [row for row in results if row[self.header.index(field)] == value]
        elif type == '<>':    
            results = [row for row in results if row[self.header.index(field)] != value]
        elif type == '<':
            results = [row for row in results if row[self.header.index(field)] < value]
        elif type == '<=':
            results = [row for row in results if row[self.header.index(field)] <= value]
        elif type == '>':
            results = [row for row in results if row[self.header.index(field)] > value]
        elif type == '>=':
            results = [row for row in results if row[self.header.index(field)] >= value]
        elif type == 'btw':
            results = [row for row in results if value <= row[self.header.index(field)] <= value2]
        elif type == 'in':
            results = [row for row in results if value in row[self.header.index(field)]]
        else:
            raise ValueError(f"Unknown WHERE type: {type}")

    def _wherelen(self, query, results):
        type = query[1]
        field = query[2]
        value = query[3]
        value2 = query[4] if type == 'btw' else None

        if type == '==' :
            results = [row for row in results if len(row[self.header.index(field)]) == value]
        elif type == '<>':
            results = [row for row in results if len(row[self.header.index(field)]) != value]
        elif type == '<':
            results = [row for row in results if len(row[self.header.index(field)]) < value]
        elif type == '<=':
            results = [row for row in results if len(row[self.header.index(field)]) <= value]
        elif type == '>':
            results = [row for row in results if len(row[self.header.index(field)]) > value]
        elif type == '>=':
            results = [row for row in results if len(row[self.header.index(field)]) >= value]
        elif type == 'btw':
            results = [row for row in results if value <= len(row[self.header.index(field)]) <= value2]
        else:
            raise ValueError(f"Unknown WHERELEN type: {type}")

    def _sort(self, query, results):
        type = query[1]
        field = query[2]
        reverse = True if type == 'r' else False

        results.sort(key=lambda row: row[self.header.index(field)], reverse=reverse)
    
    def _group(self, query, results):
        field = query[1]
        groups = dict()
        for row in results:
            value = row[self.header.index(field)]
            if value not in groups.keys():
                groups[value] = []
            groups[value].append(row)
        results = groups

    def execute(self, queries):
        self._sort_queries(queries)
        results = []
        for query in queries:
            type = query[0]
            if type == 'WHERE':
                self._where(query, results)
            elif type == 'WHERELEN':
                self._wherelen(query, results)
            elif type == 'SORT':
                self._sort(query, results)
            elif type == 'GROUP':
                self._group(query, results)
            else:
                raise ValueError(f"Unknown query type: {type}")
        return results
