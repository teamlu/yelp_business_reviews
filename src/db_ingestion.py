# db_ingest.py

from dotenv import load_dotenv
import os

load_dotenv()

from sqlalchemy import (
    create_engine, 
    Column, 
    Float,
    Integer,
    String, 
    Date, 
    MetaData, 
    func,
    text
    )
from clickhouse_sqlalchemy import (
    make_session, 
    get_declarative_base, 
    types, 
    engines
    )
import pandas as pd

ch_user = os.environ.get('CH_USER')
ch_password = os.environ.get('CH_PASSWORD')
ch_host = os.environ.get('CH_HOST')
ch_port = os.environ.get('CH_PORT')

# Connection string for ClickHouse
ch_engine = create_engine(f'clickhouse://{ch_user}:{ch_password}@{ch_host}:{ch_port}/default?protocol=https')

# Create a metadata instance and a declarative base
metadata = MetaData(bind=ch_engine)
Base = get_declarative_base(metadata=metadata)

# IMPORTANT: If the composite key used in ReplacingMergeTree (defined in order_by)
# changes, you MUST drop the existing table before running future pipelines.
# Failure to do so may result in new rows not being added correctly due to the
# changed key structure.

class BusinessData(Base):
    __tablename__ = 'business_data'
    business_id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    stars = Column(Float)
    review_count = Column(Integer)
    is_open = Column(types.UInt8)
    categories = Column(String)
    is_shopping = Column(types.UInt8)
    is_home_services = Column(types.UInt8)
    is_beauty_and_spas = Column(types.UInt8)
    is_nightlife = Column(types.UInt8)
    is_health_and_medical = Column(types.UInt8)
    is_local_services = Column(types.UInt8)
    is_bars = Column(types.UInt8)
    is_automotive = Column(types.UInt8)
    is_event_planning_and_services = Column(types.UInt8)
    is_sandwiches = Column(types.UInt8)
    is_american_traditional = Column(types.UInt8)
    is_active_life = Column(types.UInt8)
    is_pizza = Column(types.UInt8)
    is_coffee_and_tea = Column(types.UInt8)
    is_fast_food = Column(types.UInt8)
    is_breakfast_and_brunch = Column(types.UInt8)
    is_american_new = Column(types.UInt8)
    is_hotels_and_travel = Column(types.UInt8)
    is_home_and_garden = Column(types.UInt8)
    is_fashion = Column(types.UInt8)
    version = Column(types.UInt32, default=func.now())
    __table_args__ = (
        engines.ReplacingMergeTree(order_by=['business_id']),
    )

class ReviewData(Base):
    __tablename__ = 'review_data'
    review_id = Column(String, primary_key=True)
    user_id = Column(String)
    business_id = Column(String)
    stars = Column(Float)
    useful = Column(Integer)
    funny = Column(Integer)
    cool = Column(Integer)
    text = Column(String)
    date = Column(Date)
    sentiment_score = Column(Float)
    version = Column(types.UInt32, default=func.now())
    __table_args__ = (
        engines.ReplacingMergeTree(order_by=['review_id']),
    )

# Instantiate a session
session = make_session(ch_engine)

# Create tables in the database, if they don't exist
metadata.create_all(ch_engine)

# Load into database
def load_data(df: pd.DataFrame, table_class, engine: ch_engine):
    data = df.to_dict(orient='records')

    # Insert data
    with engine.connect() as conn:
        insert_statement = table_class.__table__.insert()
        conn.execute(insert_statement, data)

        # Deduplicate rows based on the version column
        # CAUTION: The 'OPTIMIZE TABLE ... FINAL' command is resource-intensive 
        # and could affect ClickHouse performance if overused. Monitor it.
        optimize_query = text(f"OPTIMIZE TABLE {table_class.__tablename__} FINAL")
        conn.execute(optimize_query)
        