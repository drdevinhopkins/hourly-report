import pandas as pd
from prophet import Prophet
import datetime

import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

forecasts = deta.Drive("forecasts")

df = pd.read_csv('data/since-2020.csv')
df.ds = pd.to_datetime(df.ds)

df = df.dropna(axis=0)

output = pd.DataFrame()

for column in df.columns.to_list():
    if column in ['Date', 'Time', 'ds']:
        continue
    try:
        # column = 'Total Inflow hrly'
        print('working on '+column)
        df2 = df[['ds', column]]
        df2.columns = ['ds', 'y']
        df2 = df2.reset_index(drop=True)
        m = Prophet(interval_width=0.95)
        m.fit(df2)
        future = m.make_future_dataframe(periods=24*7, freq='H')
        forecast = m.predict(future.tail(24*14))
        output['ds'] = forecast['ds']
        forecast = forecast[['yhat', 'yhat_lower', 'yhat_upper']]
        for forecast_column in forecast.columns.tolist():
            output[column+'_'+forecast_column] = forecast[forecast_column]
    except:
        print(column + ' failed')

output.to_csv('data/forecast.csv', index=False)

for file in ['forecast.csv']:
    forecasts.put(file, path='data/'+file)
