# Ну мне всё равно хочется написать тест хоть как просто скрипт
# Иначе непонятно, работает ли вообще

from DataProcessor import DataProcessor

if __name__ == '__main__':
    data_processor = DataProcessor().filter('filter_by', 'should_pass').sort('sort_by').group('group_by')

    print(data_processor.process([{'filter_by': 'should_pass', 'sort_by': 1, 'group_by': 2},
                                  {'filter_by': 'should_not_pass', 'sort_by': 4, 'group_by': 2},
                                  {'filter_by': 'should_pass', 'sort_by': 5, 'group_by': 1},
                                  {'filter_by': 'should_pass', 'sort_by': 2, 'group_by': 1},
                                  {'filter_by': 'should_not_pass', 'sort_by': 3, 'group_by': 5}]))
