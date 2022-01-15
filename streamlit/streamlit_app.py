import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title("Hourly Report")

df = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/recent-clean.csv')

df.ds = pd.to_datetime(df.ds)

forecast = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/forecast.csv')

forecast.ds = pd.to_datetime(forecast.ds)
# df = df.set_index('ds').head(36)

current = df.iloc[0]

current_ds = df.head(1).iloc[0].ds

st.write(df.head(1).set_index('ds').drop(['Date', 'Time'], axis=1))

st.header('Alerts')

# st.subheader('Current')

current_forecast = forecast.set_index('ds').loc[current_ds]

for column in df.columns.tolist():
    if column in ['Date', 'Time', 'ds']:
        continue
    if current[column] > current_forecast[column+'_yhat_upper']:
        st.write(column + ': ' + str(current[column]) + ' (' +
                 str(round(current_forecast[column+'_yhat_upper'], 1)) + ')')
recent_alerts = st.expander('History (last 4 hours)')
with recent_alerts:
    # st.subheader('Last 4 hours')
    for lag in [1, 2, 3, 4]:
        target_report = df.iloc[lag]
        target_forecast = forecast.set_index('ds').loc[target_report.ds]
        st.markdown('**'+str(target_report.ds)+'**')
        for column in df.columns.tolist():
            if column in ['Date', 'Time', 'ds']:
                continue
            if target_report[column] > target_forecast[column+'_yhat_upper']:
                st.write(column + ': ' + str(target_report[column]) + ' (' +
                         str(round(target_forecast[column+'_yhat_upper'], 1)) + ')')

st.header('Inflow')

# st.subheader('Today')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total", value=current['Total Inflow cum'],
              delta=int(current['Total Inflow hrly']))

with col2:
    st.metric(label="Stretcher", value=current['Stretcher Pts cum'],
              delta=int(current['Stretcher Pts hrly']))

with col3:
    st.metric(label="Ambulatory", value=current['Ambulatory Pts cum'],
              delta=int(current['Ambulatory Pts hrly']))

with col4:
    st.metric(label="Ambulances", value=current['Ambulances cum'],
              delta=int(current['Ambulances hrly']))


today = pd.to_datetime("today").date()

# inflow_chart_select = st.multiselect('',
#                                      ['Total Inflow hrly', 'Total Inflow cum', 'Stretcher Pts hrly', 'Ambulatory Pts hrly', 'Ambulances hrly'])
# inflow_chart_hrly_cum = st.radio('', ['hrly', 'cum'])
fig = make_subplots(specs=[[{"secondary_y": True}]])
# for inflow_line in inflow_chart_select:
# fig.add_trace(go.Scatter(x=df.ds, y=df[inflow_line], mode='lines',
#                          name=inflow_line, showlegend=True))
fig.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
                         ['Total Inflow hrly'], mode='lines', name='Hourly Inflow', showlegend=False), secondary_y=False)
fig.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
                         ['Total Inflow cum'], mode='lines', name='Total Inflow', showlegend=False), secondary_y=True)
# fig.add_trace(go.Scatter(x=df.index, y=df['Ambulatory Pts hrly'], mode='lines',
#                          name='Stretcher Inflow', showlegend=True))
fig.update_yaxes(title_text="Hourly Inflow", secondary_y=False)
fig.update_yaxes(title_text="Total Inflow", secondary_y=True)

st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
