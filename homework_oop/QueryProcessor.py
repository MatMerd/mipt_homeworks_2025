from collections import defaultdict


class QueryProcessor:
    def __init__(self, data):
        self.data = data
        self.operations = []

    def filter(self, field, value):
        self.operations.append({"type" : "filter", "field" : field, "value" : value})
        return self


    def sort_by(self, row, order):
        self.operations.append({"type" : "sort_by", "row" : row, "order" : order})
        return self

    def group_by(self, field):
        self.operations.append({"type" : "group_by", "field" : field})
        return self

    def execute(self):
        filter_array = [i for i in self.operations if i["type"] == "filter"]
        sort_array = [i for i in self.operations if i["type"] == "sort_by"]
        group_array = [i for i in self.operations if i["type"] == "group_by"]

        for item in filter_array:
            self.data = self.__filter_pr(item["field"], item["value"])

        for item in sort_array:
            self.data = self.__sort_pr(item["row"], item["order"])

        if group_array:
            return self.__group_pr(group_array[0]["field"])
        else:
            return self.data



    def __filter_pr(self, field, value):
        if not self.data:
            return {}

        headers = self.data[0]
        try:
            field_id = headers.index(field)
        except ValueError:
            raise ValueError(f"Field '{field}' not found in headers")

        if type(self.data[1][field_id]) != type(str(value)):
            raise ValueError(f"value in field and value have different values")
        new_data = []
        new_data.append(self.data[0])
        for item in self.data:
            # print(item[field_id])
            if item[field_id] == str(value):
                new_data.append(item)
        return new_data

    def __sort_pr(self, field, order = "asc"):
        if not self.data:
            return {}

        headers = self.data[0]
        try:
            field_index = headers.index(field)
        except ValueError:
            raise ValueError(f"Field '{field}' not found in headers")

        if order != "asc" and order != "desc":
            raise ValueError(f"order can not be {order}, use: asc, desc")
        reverse = (order == 'desc')

        return [headers] + sorted(self.data[1:], key=lambda x : int(x[field_index]), reverse=reverse)

    def __group_pr(self, field):
        if not self.data:
            return {}

        headers = self.data[0]
        try:
            field_index = headers.index(field)
        except ValueError:
            raise ValueError(f"Field '{field}' not found in headers")

        groups = defaultdict(list)
        for row in self.data[1:]:
            key = row[field_index]
            groups[key].append(row)

        return dict(groups)
