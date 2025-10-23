class QueryExecutor:
    def __init__(self, header, field_idx, indexer=None):
        self.header = header
        self.field_idx = field_idx
        self.indexer = indexer

    def _where(self, query, rows):
        _, op, field, *values = query
        value = values[0]
        idx = self.field_idx[field]

        if op == "==" and self.indexer and field in self.indexer.indexes and not rows:
            return self.indexer.get_indexed_rows(field, value)

        def match(row):
            val = row[idx]
            if op == "==": return val == value
            if op == "<>": return val != value
            if op == "<": return val < value
            if op == "<=": return val <= value
            if op == ">": return val > value
            if op == ">=": return val >= value
            raise ValueError(f"Unknown WHERE op: {op}")

        return [row for row in rows if match(row)]

    def _wherelen(self, query, rows):
        _, op, field, *values = query
        value = values[0]
        idx = self.field_idx[field]

        def match(row):
            l = len(row[idx])
            if op == "==": return l == value
            if op == "<>": return l != value
            if op == "<": return l < value
            if op == "<=": return l <= value
            if op == ">": return l > value
            if op == ">=": return l >= value
            raise ValueError(f"Unknown WHERELEN op: {op}")

        return [row for row in rows if match(row)]

    def _sort(self, query, rows):
        _, order, field = query
        reverse = (order == "r")
        idx = self.field_idx[field]
        return sorted(rows, key=lambda row: row[idx], reverse=reverse)

    def execute(self, rows, queries):
        queries = self._sort_queries(queries)

        results = []
        for query in queries:
            qtype = query[0]
            if qtype == "WHERE":
                results = self._where(query, results)
            elif qtype == "WHERELEN":
                results = self._wherelen(query, results)
            elif qtype == "SORT":
                results = self._sort(query, results)
        return results

    def _sort_queries(self, queries):
        PRIORITY = {
            "WHERE_INDEXED": 0,
            "WHERE": 1,
            "WHERELEN": 2,
            "SORT": 3
        }

        sorted_queries = []

        for q in queries:
            qtype = q[0]
            if qtype == "WHERE":
                field = q[2]
                if self.indexer and field in self.indexer.indexes:
                    priority = PRIORITY["WHERE_INDEXED"]
                else:
                    priority = PRIORITY["WHERE"]
            else:
                priority = PRIORITY[qtype]

            sorted_queries.append((priority, q))

        sorted_queries.sort(key=lambda x: x[0])
        return [q for _, q in sorted_queries]