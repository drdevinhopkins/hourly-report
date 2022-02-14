from asyncio import futures
import pandas as pd
from prophet import Prophet
import datetime

df = pd.read_csv('data/daily-visits.csv')
df.ds = pd.to_datetime(df.ds)

m = Prophet(interval_width=0.80)
m.fit(df)
future = m.make_future_dataframe(periods=14, freq='D')
forecast = m.predict(future)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

forecast.to_csv('data/daily-visits-forecast.csv', index=False)
