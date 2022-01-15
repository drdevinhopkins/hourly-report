import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title("Hourly Report")

df = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/recent-clean.csv')

forecast = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/forecast.csv')

# df = df.set_index('ds').head(36)

current = df.iloc[0]

current_ds = df.head(1).iloc[0].ds

st.write(df.head(5))

st.header('Alerts')

st.subheader('Current')

current_forecast = forecast.set_index('ds').loc[current_ds]

for column in df.columns.tolist():
    if column in ['Date', 'Time', 'ds']:
        continue
    if current[column] > current_forecast[column+'_yhat_upper']:
        st.write(column + ': ' + str(current[column]) + ' (' +
                 str(round(current_forecast[column+'_yhat_upper'], 1)) + ')')

st.subheader('Last 4 hours')
for lag in [1, 2, 3, 4]:
    target_report = df.iloc[lag]
    target_forecast = forecast.set_index('ds').loc[target_report.ds]
    st.markdown('**'+target_report.ds+'**')
    for column in df.columns.tolist():
        if column in ['Date', 'Time', 'ds']:
            continue
        if target_report[column] > target_forecast[column+'_yhat_upper']:
            st.write(column + ': ' + str(target_report[column]) + ' (' +
                     str(round(target_forecast[column+'_yhat_upper'], 1)) + ')')

st.header('Inflow')

st.subheader('Today')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total", value=df['Total Inflow cum'].tolist()[0],
              delta=df['Total Inflow cum'].tolist()[0]-df['Total Inflow cum'].tolist()[1])

with col2:
    st.metric(label="Stretcher", value=df['Stretcher Pts cum'].tolist()[0],
              delta=df['Stretcher Pts cum'].tolist()[0]-df['Stretcher Pts cum'].tolist()[1])

with col3:
    st.metric(label="Ambulatory", value=df['Ambulatory Pts cum'].tolist()[0],
              delta=df['Ambulatory Pts cum'].tolist()[0]-df['Ambulatory Pts cum'].tolist()[1])

with col4:
    st.metric(label="Ambulances", value=df['Ambulances cum'].tolist()[0],
              delta=df['Ambulances cum'].tolist()[0]-df['Ambulances cum'].tolist()[1])

inflow_chart_select = st.multiselect('',
                                     ['Total Inflow hrly', 'Total Inflow cum', 'Stretcher Pts hrly', 'Ambulatory Pts hrly', 'Ambulances hrly'])
# inflow_chart_hrly_cum = st.radio('', ['hrly', 'cum'])
fig = go.Figure()
for inflow_line in inflow_chart_select:
    fig.add_trace(go.Scatter(x=df.ds, y=df[inflow_line], mode='lines',
                             name=inflow_line, showlegend=True))
# fig.add_trace(go.Scatter(x=df.index, y=df['Stretcher Pts hrly'], mode='lines',
#                          name='Stretcher Inflow', showlegend=True))
# fig.add_trace(go.Scatter(x=df.index, y=df['Ambulatory Pts hrly'], mode='lines',
#                          name='Stretcher Inflow', showlegend=True))
st.plotly_chart(fig)
