# yelp_loading.py

import json
import pandas as pd

class YelpDataLoader:
    """Handles loading and preprocessing Yelp dataset files."""
    
    def __init__(self, downloads_path):
        self.downloads_path = downloads_path

    def load_json_file(self, filename):
        """Loads a single line-delimited JSON file as a DataFrame."""
        with open(f"{self.downloads_path}/{filename}", 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
        return pd.DataFrame(data)

    def load_filtered_review_file(self, filename, start_year=2020, end_year=2022):
        """Loads and filters the review dataset based on a date range."""
        with open(f"{self.downloads_path}/{filename}", 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file if 'date' in json.loads(line)]
        filtered_data = [review for review in data if int(review['date'][:4]) in range(start_year, end_year + 1)]
        return pd.DataFrame(filtered_data)
