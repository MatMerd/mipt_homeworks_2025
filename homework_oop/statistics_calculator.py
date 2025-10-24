import statistics
from typing import List, Dict, Any

from DataProcessor import CsvTable


class StatisticsCalculator:

    def __init__(self, data: CsvTable):
        self._data = data

    def median_size(self) -> float:
        sizes = []
        for row in self._data:
            try:
                size = row['Size']
                if size is not None and size != '':
                    sizes.append(int(size))
            except KeyError:
                raise ValueError("Данные не содержат обязательного поля 'Size'")
            except (ValueError, TypeError):
                continue

        if not sizes:
            raise ValueError("Не найдено ни одного корректного значения размера репозитория.")

        return statistics.median(sizes)

    def most_starred_repositories(self, top_n: int = 10) -> List[Dict[str, Any]]:
        for row in self._data:
            if 'Stars' not in row:
                raise ValueError("Данные не содержат обязательного поля 'Stars'")

        sorted_data = sorted(
            self._data,
            key=lambda x: int(x['Stars']) if x['Stars'] not in (None, '') else 0,
            reverse=True
        )

        return sorted_data[:top_n]

    def repositories_without_language(self) -> List[Dict[str, Any]]:
        for row in self._data:
            if 'Language' not in row:
                raise ValueError("Данные не содержат обязательного поля 'Language'")

        return [row for row in self._data if row['Language'] in (None, '', ' ')]

    def max_stars_count(self) -> int:
        stars_list = []
        for row in self._data:
            try:
                stars = row['Stars']
                if stars is not None and stars != '':
                    stars_list.append(int(stars))
            except KeyError:
                raise ValueError("Данные не содержат обязательного поля 'Stars'")
            except (ValueError, TypeError):
                continue

        if not stars_list:
            raise ValueError("Не найдено ни одного корректного значения количества звезд.")

        return max(stars_list)

    def custom_statistics(self, field_name: str, aggregation_func: callable) -> Any:
        values = []
        for row in self._data:
            if field_name not in row:
                raise ValueError(f"Данные не содержат поля '{field_name}'")
            value = row[field_name]
            if value not in (None, ''):
                try:
                    if aggregation_func in [sum, max, min, statistics.mean, statistics.median]:
                        values.append(int(value))
                    else:
                        values.append(value)
                except (ValueError, TypeError):
                    continue

        if not values:
            raise ValueError(f"Не найдено ни одного корректного значения для поля '{field_name}'.")

        return aggregation_func(values)

    def comprehensive_stats(self) -> Dict[str, Any]:
        stats = {}
        try:
            stats['median_size'] = self.median_size()
        except ValueError as e:
            stats['median_size'] = f"Ошибка: {e}"

        try:
            stats['max_stars'] = self.max_stars_count()
        except ValueError as e:
            stats['max_stars'] = f"Ошибка: {e}"

        try:
            stats['repositories_without_language'] = len(self.repositories_without_language())
        except ValueError as e:
            stats['repositories_without_language'] = f"Ошибка: {e}"

        try:
            forks_list = [int(row['Forks']) for row in self._data if row['Forks'] not in (None, '')]
            if forks_list:
                stats['average_forks'] = round(statistics.mean(forks_list), 2)
            else:
                stats['average_forks'] = 0
        except (ValueError, KeyError) as e:
            stats['average_forks'] = f"Ошибка: {e}"

        return stats
