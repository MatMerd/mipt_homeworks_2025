import csv
from dataclasses import asdict
from typing import List, Dict, Any, Union
from datacls import QueryStats

def stats_to_csv(data: Union[QueryStats, List[QueryStats]], filename: str) -> None:
    if not data:
        return
    
    if isinstance(data, QueryStats):
        data_list = [data]
    else:
        data_list = data
    
    dict_list = []
    for item in data_list:
        if isinstance(item, QueryStats):
            if hasattr(item, '__dict__'):
                dict_list.append(item.__dict__)
            else:
                dict_list.append((item))
    
    if not dict_list:
        return

    fieldnames = dict_list[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_list)