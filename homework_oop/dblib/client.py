import copy
import csv
from dataclasses import dataclass, field

from .connect import *
import numpy as np


@dataclass
class Client:
    connections : dict[int, DBConnect] = field(default_factory=dict)
    saved_queries : dict[str, dict] = field(default_factory=dict)
    _total_connections_count : int = 0

    def _get_new_index(self):
        self._total_connections_count += 1
        return self._total_connections_count

    def connect(self, file_name : str):
        id_ = self._get_new_index()
        self.connections[id_] = DBConnect(file_name)
        return id_


    def close(self, ind : int):
        if ind in self.connections:
            del self.connections[ind]
        else:
            raise self.NoConnectionFound(f"No open connection with id = {ind}")

    class NoConnectionFound(Exception): pass

    class InvalidArgumentNumber(Exception): pass

    class InvalidArgument(Exception): pass

    class DataManager:

        def __init__(self, data, headers):
            self._headers_names : list[str] = headers
            self._data : list[dict] = [dict(zip(self._headers_names, row)) for row in data]

        class InvalidArgument(Exception): pass

        def select(self, *column_names):
            for col_name in column_names:
                if not col_name in self._headers_names:
                    raise self.InvalidArgument(f"No column named {col_name}")
            return [{key : row[key] for key in column_names} for row in self._data]

        def get_data(self):
            return copy.deepcopy(self._data)

        def median_repository_size(self):
            repositories_size = [row["Size"] for row in self._data]
            return np.median(repositories_size)

        def most_liked_repository(self):
            rows = [r for r in self._data if r["Stars"] is not None]
            if not rows:
                raise self.InvalidArgument("No non-null 'Stars' values")
            return max(rows, key=lambda r: r["Stars"]).copy()

        def repositories_without_language(self):
            return [row.copy() for row in self._data if not row["Language"]]

        def top_repositories_by_watchers(self, top = 10):
            rows = [r for r in self._data if r.get("Watchers") is not None]
            rows.sort(key=lambda d: d["Watchers"], reverse=True)
            return [r.copy() for r in rows[:top]]

        def save_data_in_csv(self, data : list[dict], path : str):
            if not data:
                raise ValueError("Data is empty")
            headers = data[0].keys()
            with open(path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

    def saved_query(self, name : str):
        if not name in self.saved_queries:
            raise self.InvalidArgument(f"No saved query named {name}")
        query = self.saved_queries[name]
        return self.query(connection_ind=query["connection_ind"], where_val=query["where_val"], where_col=query["where_col"], order_by=query["order_by"])

    def delete_query(self, name : str):
        if not name in self.saved_queries:
            raise self.InvalidArgument(f"No saved query named {name}")
        del self.saved_queries[name]

    def query(self, connection_ind : int = None, where_val : list[tuple] = None, where_col : list[tuple] = None, order_by : list[tuple] = None, save : str | None = None):
        if save:
            self.saved_queries[save] = {"connection_ind" : connection_ind, "where_val" : where_val, "where_col" : where_col, "order_by" : order_by}
        if connection_ind is None or not connection_ind in self.connections:
            raise self.NoConnectionFound(f"No connect with {connection_ind=}")
        connection = self.connections[connection_ind]
        if not where_val is None:
            for where_query in where_val:
                if len(where_query) != 3:
                    raise self.InvalidArgumentNumber(f"where_val expected 3 arguments, got {len(where_query)} : {where_query}")
                if where_query[1] not in ["<", "<=", ">", ">=", "=="]:
                    raise self.InvalidArgument(f"Not suitable operator {where_query[1]}")
                connection.add_query(("WHERE", where_query[1], where_query[0], where_query[2]))
        if not where_col is None:
            for where_query in where_col:
                if len(where_query) != 3:
                    raise self.InvalidArgumentNumber(f"where_col expected 3 arguments, got {len(where_query)} : {where_query}")
                if where_query[1] not in ["<", "<=", ">", ">=", "=="]:
                    raise self.InvalidArgument(f"Not suitable operator {where_query[1]}")
                connection.add_query(("WHERECOL", where_query[1], where_query[0], where_query[2]))
        if not order_by is None:
            for order_by_query in order_by:
                if len(order_by_query) != 2:
                    raise self.InvalidArgumentNumber(f"order_by expected 2 arguments, got {len(order_by_query)} : {order_by_query}")
                if order_by_query[1] not in [True, False]:
                    raise self.InvalidArgument(f"The sorting order in order_by is not clear : {order_by_query[1]} not a boolean True or False")
                if order_by_query[1]:
                    connection.add_query(("SORT", "r", order_by_query[0]))
                else:
                    connection.add_query(("SORT", "n", order_by_query[0]))
        return self.DataManager(connection.execute(), connection.get_headers())