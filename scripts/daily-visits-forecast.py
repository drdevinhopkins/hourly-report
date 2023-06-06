from asyncio import futures
import pandas as pd
from prophet import Prophet
import datetime

import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

forecasts = deta.Drive("forecasts")

df = pd.read_csv('data/daily-visits.csv')
df.ds = pd.to_datetime(df.ds)
df = df[df.ds >= '2020-02-01']

m = Prophet(interval_width=0.80,
            changepoint_prior_scale=10,
            seasonality_prior_scale=0.01,
            seasonality_mode='multiplicative',
            holidays_prior_scale=0.1,
            changepoint_range=0.95,
            n_changepoints=50).add_country_holidays(country_name='CA')
m.fit(df)
future = m.make_future_dataframe(periods=14, freq='D')
forecast = m.predict(future)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

forecast.to_csv('data/daily-visits-forecast.csv', index=False)

for file in ['daily-visits.csv', 'daily-visits-forecast.csv']:
    forecasts.put(file, path='data/'+file)
