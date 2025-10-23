from dataclasses import dataclass, field
from .connect import *


@dataclass
class Client:
    connections : dict[int, DBConnect] = field(default_factory=dict[int, DBConnect])
    saved_queries : list[tuple] = field(default_factory=list[tuple])
    _total_connections_count = 0

    def _GetNewIndex(self):
        self._total_connections_count += 1
        return self._total_connections_count

    def Connect(self, file_name : str):
        id_ = self._GetNewIndex()
        self.connections[id_] = DBConnect(file_name)
        return id_


    def Close(self, ind : int):
        del self.connections[ind]

    class NoConnectionFound(Exception):
        def __init__(self, error):
            self.error = error
        def __str__(self):
            return self.error

    class InvalidArgumentNumber(Exception):
        def __init__(self, error):
            self.error = error
        def __str__(self):
            return self.error

    class InvalidArgument(Exception):
        def __init__(self, error):
            self.error = error
        def __str__(self):
            return self.error

    @dataclass
    class DataManager:
        data : list[tuple]
        headers_names : list[str]

        class InvalidArgument(Exception):
            def __init__(self, error):
                self.error = error

            def __str__(self):
                return self.error

        def Select(self, select : list[str]):
            query = []
            for col_name in select:
                if not col_name in self.headers_names:
                    raise self.InvalidArgument(f"No column named {col_name}")
            for data_line in self.data:
                new_line = []
                for ind, col_name in enumerate(self.headers_names):
                    if col_name in select:
                        new_line.append(data_line[ind])
                query.append(new_line)
            return query

        def GetData(self):
            return self.data

    def Query(self, connection_ind : int = None, where_val : list[tuple] = None, where_col : list[tuple] = None, order_by : list[tuple] = None):
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
                    raise self.InvalidArgumentNumber(f"where_cal expected 3 arguments, got {len(where_query)} : {where_query}")
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