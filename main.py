# main.py

import os
from dotenv import load_dotenv
from tqdm.auto import tqdm

from src.yelp_loading import YelpDataLoader
from src.data_processing import DataFormatter
from src.db_ingestion import load_data, BusinessData, ReviewData, ch_engine

load_dotenv()

def main():
    downloads_path = os.getenv('MY_DIR')
    loader = YelpDataLoader(downloads_path)

    # Loading data
    tqdm.write("Loading Review Data...")
    review_data = loader.load_filtered_review_file('yelp_academic_dataset_review.json')
    
    tqdm.write("Loading Business Data...")
    business_data = loader.load_json_file('yelp_academic_dataset_business.json')

    # Processing data
    tqdm.write("Processing Data...")
    formatter = DataFormatter(business_data, review_data)
    
    tqdm.write("Adding Sentiment Scores...")
    formatter.add_sentiment_scores()
    
    tqdm.write("Adding Category Fields...")
    formatter.add_category_fields()
    
    tqdm.write("Removing JSON Type Fields...")
    formatter.remove_json_fields()

    # Ingesting data
    tqdm.write("Ingesting Business Data...")
    load_data(business_data, BusinessData, ch_engine)
    
    tqdm.write("Ingesting Review Data...")
    load_data(review_data, ReviewData, ch_engine)

    tqdm.write("** Completed All Processes **")

if __name__ == "__main__":
    main()
