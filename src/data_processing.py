# data_processing.py

from textblob import TextBlob
from tqdm import tqdm

tqdm.pandas()

class SentimentAnalyzer:
    """Performs sentiment analysis on text data."""
    @staticmethod
    def calculate_sentiment(text):
        """Calculates sentiment score of text."""
        blob = TextBlob(text)
        return (blob.sentiment.polarity + 1) * 50  # scale from [-1,1] to [0,100]

class DataFormatter:
    """Formats and merges Yelp datasets for analysis."""
    def __init__(self, business_data, review_data):
        self.business_data = business_data
        self.review_data = review_data

    def add_sentiment_scores(self):
        """Adds sentiment scores to review data with progress bar."""
        self.review_data['sentiment_score'] = self.review_data['text'].progress_apply(SentimentAnalyzer.calculate_sentiment)
        
    def add_category_fields(self, top_n=20):
        """Adds fields for top categories to the combined DataFrame."""
        category_counts = self.business_data['categories'].str.split(', ') \
            .explode() \
            .value_counts() \
            .drop(labels=['Food', 'Restaurants'])
        top_categories = category_counts.head(top_n).index

        for category in top_categories:
            field_name = f'is_{category.lower().replace(" ", "_").replace("&", "and")}'
            self.business_data[field_name] = self.business_data['categories'].str.contains(category, case=False, na=False)

        [col.replace('(', '').replace(')', '') for col in self.business_data.columns]
    
    def remove_json_fields(self):
        """Removes JSON-like fields from business_data."""
        if 'attributes' in self.business_data.columns:
            del self.business_data['attributes']
        if 'hours' in self.business_data.columns:
            del self.business_data['hours']
