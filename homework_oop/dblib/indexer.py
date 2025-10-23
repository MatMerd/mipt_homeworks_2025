class Indexer:
    def __init__(self, rows, header, index_fields=()):
        self.rows = rows
        self.header = header
        self.index_fields = index_fields
        self.indexes = {}
        self.field_idx = {name: i for i, name in enumerate(header)}
        self.create_indexes()

    def create_indexes(self):
        for field in self.index_fields:
            idx = self.field_idx[field]
            index = {}
            for i, row in enumerate(self.rows):
                key = row[idx]
                index.setdefault(key, []).append(i)
            self.indexes[field] = index

    def get_indexed_rows(self, field, value):
        if field not in self.indexes:
            return None
        indexes = self.indexes[field].get(value, [])
        return [self.rows[i] for i in indexes]