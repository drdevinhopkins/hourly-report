import pandas as pd
import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

data = deta.Drive("data")

old_weather = pd.read_csv('data/weatherArchiveAndForecast.csv')
old_weather.ds = pd.to_datetime(old_weather.ds)

forecast = pd.read_csv(
    'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/montreal/next24hours?unitGroup=metric&include=hours&key=RGEY54DWN2UNQWC86N2UVF4CU&contentType=csv')
forecast = forecast.rename(columns={'datetime': 'ds'})
forecast.ds = pd.to_datetime(forecast.ds)

new_weather = pd.concat(
    [old_weather, forecast], join='inner').drop_duplicates(subset='ds', keep='last')

new_weather.to_csv('data/weatherArchiveAndForecast.csv', index=False)


old_weather = pd.read_csv('data/daily-weather.csv')
old_weather.ds = pd.to_datetime(old_weather.ds)

forecast = pd.read_csv(
    'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/montreal?unitGroup=metric&include=days&key=RGEY54DWN2UNQWC86N2UVF4CU&contentType=csv')
forecast = forecast.rename(columns={'datetime': 'ds'})
forecast.ds = pd.to_datetime(forecast.ds)

new_weather = pd.concat(
    [old_weather, forecast], join='inner').drop_duplicates(subset='ds', keep='last')

new_weather.to_csv('data/daily-weather.csv', index=False)

data.put('weatherArchiveAndForecast.csv', path='data/weatherArchiveAndForecast.csv')
data.put('daily-weather.csv', path='data/daily-weather.csv')
