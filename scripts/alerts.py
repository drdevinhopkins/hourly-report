import pandas as pd
import pymsteams
from dotenv import load_dotenv
import os
# import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

load_dotenv()


def load_data():

    df = pd.read_csv('data/recent.csv')

    df.ds = pd.to_datetime(df.ds)

    df = df.sort_values(by='ds', ascending=False)

    forecast = pd.read_csv('data/forecast.csv')

    forecast.ds = pd.to_datetime(forecast.ds)

    current = df.tail(1).iloc[0]

    current_ds = df.ds.max()

    return df, forecast, current, current_ds


df, forecast, current, current_ds = load_data()


alert_types = [
    # 'Total Inflow hrly',
    #  'Ambulances hrly',
    'Total Stretcher pts',
    'Triage hallway pts',
    'Triage hallway pts TBS',
    #  'Resus Pts',
    #  'Totalpts in PODs except Psych',
    # 'Green Pts TBS',
    # 'Yellow Pts TBS',
    # 'Orange Pts TBS',
    # 'Consults > 2h in PODS except IM',
    # 'Consult for IM >4h in PODS',
    # 'Plain films reqs > 2 h in PODs'
    # 'CTs reqs > 2 h in PODs',
    #  'Post POD (Family room)',
    #  'QTrack Patients TBS',
    #  'GARAGE patient TBS',
    # 'Consults > 2h in Vertical Except IM',
    # 'Consult for IM >4h in Vertical',
    # 'Plain films reqs > 2 hr in Vertical',
    # 'CTs reqs > 2 hrs in Vertical',
    'Total Pod TBS',
    'Total Vertical TBS']

alert_categories = {
    # 'Total Inflow hrly',
    #  'Ambulances hrly',
    'Total Stretcher pts': 'Patient Volume',
    'Triage hallway pts': 'Patient Volume',
    'Triage hallway pts TBS': 'Patient Volume',
    #  'Resus Pts',
    #  'Totalpts in PODs except Psych',
    # 'Green Pts TBS': 'Patient Volume',
    # 'Yellow Pts TBS',
    # 'Orange Pts TBS',
    'Consults > 2h in PODS except IM': 'Consultations',
    'Consult for IM >4h in PODS': 'Consultations',
    'Plain films reqs > 2 h in PODs': 'Radiology',
    'CTs reqs > 2 h in PODs': 'Radiology',
    #  'Post POD (Family room)',
    #  'QTrack Patients TBS',
    #  'GARAGE patient TBS',
    'Consults > 2h in Vertical Except IM': 'Consultations',
    'Consult for IM >4h in Vertical': 'Consultations',
    'Plain films reqs > 2 hr in Vertical': 'Radiology',
    'CTs reqs > 2 hrs in Vertical': 'Radiology',
    'Total Pod TBS': 'Patient Volume',
    'Total Vertical TBS': 'Patient Volume'}


def create_fig(df, forecast, metric):

    fig = make_subplots(
        specs=[[{"secondary_y": True}]], subplot_titles=[metric])

    fig.add_trace(go.Scatter(x=forecast.ds, y=forecast
                             [metric+'_yhat'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='blue', width=1, dash='dot'), fill='tozeroy', fillcolor='lightgreen'))
    fig.add_trace(go.Scatter(x=forecast.ds, y=forecast
                             [metric+'_yhat_upper'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='blue', width=1, dash='dot'), fill='tonexty', fillcolor='lightyellow'))
    fig.add_trace(go.Scatter(x=forecast.ds, y=forecast
                             [metric+'_yhat_upper']*10, mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='blue', width=1, dash='dot'), fill='tonexty', fillcolor='lightpink'))
    fig.add_trace(go.Scatter(x=forecast.ds, y=forecast
                             [metric+'_yhat_lower'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='blue', width=1, dash='dot')))

    fig.add_trace(go.Scatter(x=df.ds, y=df
                             [metric], mode='lines+markers', name=metric, showlegend=False, line=dict(color='red', width=2)))

    fig.update_xaxes(range=[df.head(8).ds.min(), df.head(8).ds.max()])
    fig.update_yaxes(range=[0, max(df.head(8)[metric].max(
    )*1.2, forecast.head(8)[metric+'_yhat_upper'].max()*1.2)])

    fig.write_image("images/{}.png".format(metric))
    return "images/{}.png".format(metric)


current_forecast = forecast.set_index('ds').loc[current_ds]


alerts = []

for column in alert_types:
    try:
        if current[column] > current_forecast[column+'_yhat_upper']:
            alerts.append({'category': alert_categories[column], 'metric': column, 'value': current[column], 'yhat_upper': round(
                current_forecast[column+'_yhat_upper'], 1)})
    except:
        continue


if alerts:
    alerts_df = pd.DataFrame(alerts)

    active_alert_categories = alerts_df.category.unique().tolist()

    myTeamsMessage = pymsteams.connectorcard(os.environ.get('TEAMS_WEBHOOK'))

    # myTeamsMessage.title("Overcrowding alert")

    myTeamsMessage.text(' ')

    for category in active_alert_categories:

        myMessageSection = pymsteams.cardsection()

        myMessageSection.title(category)

        for i, row in alerts_df[alerts_df['category'] == category].iterrows():

            myMessageSection.addFact(row['metric'], str(row['value']))

            create_fig(df, forecast, row['metric'])

        myTeamsMessage.addSection(myMessageSection)

    myTeamsMessage.printme()

    myTeamsMessage.send()

else:
    print('No alerts')
