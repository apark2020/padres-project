from config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)

df = pd.read_csv('padres_data.csv')
df.to_sql('pitch_data', con=engine, if_exists='replace', index=True)