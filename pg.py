from sqlalchemy import create_engine, text
from sqlalchemy import and_
import sqlalchemy as db
from configparser import ConfigParser
import pandas as pd
key = ".env"
parser = ConfigParser()
_ = parser.read(key)
db_url = parser.get('postgres', 'db_url')
print(db_url)
engine = create_engine(db_url)
metadata = db.MetaData()
census = db.Table('patrimonio', metadata, autoload_with=engine)
query = db.select(census)
df = pd.read_sql(con=engine.connect(), sql=query)
print(df)
