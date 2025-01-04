from config import Config
from sqlalchemy import create_engine
from sqlalchemy.types import Integer
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import sqlite3

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)

df = pd.read_csv('padres_data.csv')
df.reset_index(inplace=True)

with sqlite3.connect('pitchdata.db') as con:
    df.to_sql('pitch_data', con=con, if_exists='replace',dtype={'index':'INTEGER PRIMARY KEY AUTOINCREMENT'})

# with engine.connect() as con:
#     con.execute('ALTER TABLE pitch_data ADD PRIMARY KEY(id)')

