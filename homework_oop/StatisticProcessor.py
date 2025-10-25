from typing import List, Dict, Any
import statistics
from homework_oop.DataProcessor import DataProcessor

class StatisticsProcessor():
    def __init__(self, processor: DataProcessor):
        self.processor = processor

    def median_repository_size(self) -> float:
        data = self.processor.select('Size').execute()
        sizes = [float(row['Size']) for row in data if row.get('Size', '').isdigit()]
        return statistics.median(sizes)

    def most_starred_repository(self) -> Dict[str, str]:
        data = self.processor.sort_by('Stars', reverse=True).execute()
        return data[0] if data else {}

    def repositories_without_language(self) -> List[Dict[str, str]]:
        data = self.processor.select('Name', 'Language').execute()
        return [row for row in data if not row.get('Language') or row['Language'].strip() == '']

    def top_repositories_by_forks(self, top_n: int = 10) -> List[Dict[str, str]]:
        data = self.processor.sort_by('Forks', reverse=True).execute()
        return data[:top_n]

    def average_stars_by_language(self) -> Dict[str, float]:
        grouped = self.processor.group_by('Language').execute()
        result = {}
        for language, repos in grouped.items():
            stars = [float(r['Stars']) for r in repos if r.get('Stars', '').isdigit()]
            if stars:
                result[language or 'Unknown'] = round(sum(stars) / len(stars), 2)
        return result