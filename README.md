# Restaurant Review Sentiment Analysis

## Overview
This project conducts a detailed sentiment analysis of customer reviews for Saffron Indian Kitchen. The intent is to provide restaurant owners actionable insights using customer feedback to enhance dining experiences and operational strategies.

## Features
- Sentiment scoring of customer reviews.
- Identification of top-performing and underperforming menu items.
- Trend analysis of customer satisfaction over time.

## Data
The [dataset](https://www.yelp.com/dataset) includes customer reviews from Yelp.

## Analysis
Using Python for transformations, Clickhouse for warehousing, SQL for aggregation, and Hex for data visualization, I extract key insights for Saffron Indian Kitchen - a chain of Mom & Pop Indian restaurants in Pennsylvania.

## Insights
The analysis reveals key areas for celebration and improvement. The Murg Vindaloo and Chicken Tikka Masala recipes are flagged for refinement, while the excellent customer service and dishes like Papri Chaat and Mutter Paneer are highlighted as strengths.

## Usage
To run the analysis, follow these steps:

1. Clone the repository:
```
git clone [URL to repository]
```

2. Create a virtual environment (optional but recommended):
```
source venv/bin/activate
```

3. Install required dependencies:
```
pip install -r requirements.txt
```

4. In the root directory of your project, download `yelp_academic_dataset_business.json` and `yelp_academic_dataset_review.json`. Create an `.env` file replacing placeholders with your actual paths and credentials:
```
MY_DIR=<path_to_your_yelp_datasets_directory>
CH_HOST=<your_clickhouse_host>
CH_PORT=<your_clickhouse_port>
CH_USER=<your_clickhouse_username>
CH_PASSWORD=<your_clickhouse_password>
```

5. Execute main.py:
```
python main.py
```
