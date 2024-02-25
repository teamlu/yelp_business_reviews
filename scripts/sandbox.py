# sandbox.py
# %% 
# RUN LOCAL
import json
import pandas as pd
from textblob import TextBlob
from tqdm import tqdm

tqdm.pandas()

class YelpDataLoader:
    
    def __init__(self, downloads_path):
        self.downloads_path = downloads_path

    def load_json_file(self, filename):
        with open(f"{self.downloads_path}/{filename}", 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
        return pd.DataFrame(data)

    def load_filtered_review_file(self, filename, start_year=2020, end_year=2022):
        with open(f"{self.downloads_path}/{filename}", 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file if 'date' in json.loads(line)]
        filtered_data = [review for review in data if int(review['date'][:4]) in range(start_year, end_year + 1)]
        return pd.DataFrame(filtered_data)


class SentimentAnalyzer:

    @staticmethod
    def calculate_sentiment(text):
        blob = TextBlob(text)
        return (blob.sentiment.polarity + 1) * 50


class DataFormatter:

    def __init__(self, business_data, review_data):
        self.business_data = business_data
        self.review_data = review_data

    def add_sentiment_scores(self):
        self.review_data['sentiment_score'] = self.review_data['text'].progress_apply(SentimentAnalyzer.calculate_sentiment)
        
    def add_category_fields(self, top_n=20):
        category_counts = self.business_data['categories'].str.split(', ') \
            .explode() \
            .value_counts() \
            .drop(labels=['Food', 'Restaurants'])
        top_categories = category_counts.head(top_n).index

        for category in top_categories:
            field_name = f'is_{category.lower().replace(" ", "_").replace("&", "and")}'
            self.business_data[field_name] = self.business_data['categories'].str.contains(category, case=False, na=False)

        [col.replace('(', '').replace(')', '') for col in self.business_data.columns]

    def filter_and_merge_data(self):
        self.business_data['categories'] = self.business_data['categories'].fillna('')
        filtered_business_data = self.business_data[self.business_data['categories'].str.contains('Restaurants|Food')]
        return pd.merge(filtered_business_data, self.review_data, on='business_id', how='inner')

    @staticmethod
    def filter_by_date(combined_data, years):
        combined_data['date'] = pd.to_datetime(combined_data['date'], errors='coerce')
        return combined_data[combined_data['date'].dt.year.isin(years)]


downloads_path = '/Users/timlu/Downloads/yelp_dataset/'
loader = YelpDataLoader(downloads_path)

review_data = loader.load_filtered_review_file('yelp_academic_dataset_review.json')
checkin_data = loader.load_json_file('yelp_academic_dataset_checkin.json')
tip_data = loader.load_json_file('yelp_academic_dataset_tip.json')
user_data = loader.load_json_file('yelp_academic_dataset_user.json')
business_data = loader.load_json_file('yelp_academic_dataset_business.json')

formatter = DataFormatter(business_data, review_data)
formatter.add_sentiment_scores()
formatter.add_category_fields()
combined_data = formatter.filter_and_merge_data()
full_2020_2022 = formatter.filter_by_date(combined_data, [2020, 2021, 2022])
full_2020_2022
