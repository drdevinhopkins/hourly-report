import pandas as pd

old_weather = pd.read_csv('data/weatherArchiveAndForecast.csv')
old_weather.ds = pd.to_datetime(old_weather.ds)

forecast = pd.read_csv(
    'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/montreal/next24hours?unitGroup=metric&include=hours&key=NDD4FLZ37NRPKGD82DRZWXGHU&contentType=csv')
forecast = forecast.rename(columns={'datetime': 'ds'})
forecast.ds = pd.to_datetime(forecast.ds)

new_weather = pd.concat(
    [old_weather, forecast], join='inner').drop_duplicates(subset='ds', keep='last')

new_weather.to_csv('data/weatherArchiveAndForecast.csv', index=False)
