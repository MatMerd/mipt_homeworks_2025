import csv
from typing import List, Union
from datacls import QueryStats

def to_csv(data: List[Union[QueryStats, List[QueryStats]]], filename: str) -> None:
    if not data:
        return
    
    data_list: List[List[QueryStats]] = []
    
    for item in data:
        if isinstance(item, QueryStats):
            data_list.append([item])
        elif isinstance(item, list):
            data_list.append(item)
    
    results = []
    for items in data_list:
        dict_list = []
        for item in items:
            if isinstance(item, QueryStats):
                if hasattr(item, '__dict__'):
                    dict_list.append(item.__dict__)
                else:
                    dict_list.append((item))
        results.append(dict_list)
    
    if not results:
        return

    fieldnames = results[0][0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerows(result)