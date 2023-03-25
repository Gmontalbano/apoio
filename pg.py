import datetime
import calendar
from datetime import date

from sqlalchemy import create_engine, text, extract, and_
import sqlalchemy as db
from configparser import ConfigParser
import pandas as pd
key = ".env"
parser = ConfigParser()
_ = parser.read(key)
db_url = parser.get('postgres', 'db_url')
print(db_url)
engine = create_engine(db_url)
conn = engine.connect()
metadata = db.MetaData()
users = db.Table('users_table', metadata, autoload_with=engine)
cal = db.Table('calendario', metadata, autoload_with=engine)

username = 'teste'
password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
data = date.today()
"""query = db.insert(cal).values(evento='teste', data_inicio=data, data_fim=data)
conn.execute(query)
conn.commit()"""

year = 2023
month = 2

num_days = calendar.monthrange(year, month)[1]
start_date = datetime.date(year, month, 1)
end_date = datetime.date(year, month, num_days)
query = db.select(cal).filter(and_(cal.columns.data_inicio >= start_date, cal.columns.data_inicio <= end_date))
df = pd.read_sql(con=conn, sql=query)
print(df)
