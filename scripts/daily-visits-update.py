import pandas as pd
import datetime
import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

data = deta.Drive("data")

df = pd.read_csv('data/daily-visits.csv')
df.ds = pd.to_datetime(df.ds)

archive = pd.read_csv('data/since-2020.csv')
archive.ds = pd.to_datetime(archive.ds)
archive = archive.set_index('ds')

archive = archive[archive.index.hour == 0][['Total Inflow cum']]
archive.columns = ['y']
archive = archive.reset_index()

archive['ds'] = archive['ds'] - datetime.timedelta(days=1)

df = pd.concat([df, archive], ignore_index=True).drop_duplicates(
    keep='first').sort_values(by='ds', ascending=False).reset_index(drop=True)

df.to_csv('data/daily-visits.csv', index=False)

data.put('daily-visits.csv', path='data/daily-visits.csv')
