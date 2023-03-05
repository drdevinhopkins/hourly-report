import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

st.set_page_config(layout="wide")

df = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/recent.csv')

df.ds = pd.to_datetime(df.ds)

forecast = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/forecast.csv')

forecast.ds = pd.to_datetime(forecast.ds)

current = df.iloc[0]

current_ds = df.head(1).iloc[0].ds

daily_visits_df = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/daily-visits.csv')

daily_visits_df.ds = pd.to_datetime(daily_visits_df.ds)

daily_visits_forecast = pd.read_csv(
    'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/daily-visits-forecast.csv')

daily_visits_forecast.ds = pd.to_datetime(daily_visits_forecast.ds)

st.title('Hourly Report')
mobile = st.checkbox('Mobile version')

# SIDEBAR
st.sidebar.write('Last Update ' + str(df.iloc[0].ds))
# display = st.sidebar.selectbox('Display Type', ['Desktop', 'Mobile'])
filter_expander = st.sidebar.expander('Alert Filters')

with filter_expander:
    alert_type_select = st.multiselect('Filter by type', [
        column for column in df.columns.tolist() if column not in ['Date', 'Time', 'ds']],
        ['Total Inflow hrly',
         'Ambulances hrly',
         'Total Stretcher pts',
         'Triage hallway pts',
            'Triage hallway pts TBS',
            'Resus Pts',
            'Totalpts in PODs except Psych',
            'Green Pts TBS',
            'Yellow Pts TBS',
            'Orange Pts TBS',
            # 'Consults > 2h in PODS except IM',
            # 'Consult for IM >4h in PODS',
            # 'CTs reqs > 2 h in PODs',
            'Post POD (Family room)',
            'QTrack Patients TBS',
            'GARAGE patient TBS',
            # 'Consults > 2h in Vertical Except IM',
            # 'Consult for IM >4h in Vertical',
            # 'Plain films reqs > 2 hr in Vertical',
            # 'CTs reqs > 2 hrs in Vertical',
            'Total Pod TBS',
            'Total Vertical TBS'])

today = df.iloc[0].ds.date()

todays_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 -
                                                                               df.iloc[0].ds.hour))) & (forecast.ds > (df.iloc[0].ds + datetime.timedelta(hours=-1 -
                                                                                                                                                          df.iloc[0].ds.hour)))]

fig = make_subplots(
    specs=[[{"secondary_y": True}]], subplot_titles=['Inflow'])

fig.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
                         ['Total Inflow hrly'], mode='markers', name='Hourly Inflow', showlegend=False, line=dict(color='red', width=4)), secondary_y=False)
fig.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                         ['Total Inflow hrly_yhat_lower'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
fig.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                         ['Total Inflow hrly_yhat'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
fig.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                         ['Total Inflow hrly_yhat_upper'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)

fig.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
                         ['Total Inflow cum'], mode='lines', name='Total Inflow', showlegend=False, line=dict(color='blue', width=4)), secondary_y=True)

total_inflow_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 -
                                                                                     df.iloc[0].ds.hour))) & (forecast.ds > df.iloc[0].ds)][['ds', 'Total Inflow hrly_yhat']]

total_inflow_forecast['y'] = total_inflow_forecast['Total Inflow hrly_yhat'].astype(
    int).expanding().sum().astype(int).add(df.iloc[0]['Total Inflow cum'])

total_inflow_forecast = pd.concat([df.head(1)[['ds', 'Total Inflow cum']].rename(
    {'Total Inflow cum': 'y'}, axis=1), total_inflow_forecast])

fig.add_trace(go.Scatter(x=total_inflow_forecast.ds, y=total_inflow_forecast.y, mode='lines',
                         name='Total Inflow (expected)', showlegend=False, line=dict(color='blue', width=1, dash='dot')), secondary_y=True)

fig.update_yaxes(title_text="Hourly",
                 secondary_y=False, range=[0, max(df[df.Date == current.Date]['Total Inflow hrly'].max(), todays_forecast
                                                  ['Total Inflow hrly_yhat_upper'].max())+2])
fig.update_yaxes(title_text="Total",
                 secondary_y=True, range=[0, 300])

fig2 = make_subplots(specs=[[{"secondary_y": True}]], subplot_titles=[
    'Stretcher Occupancy'])

fig2.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
                          ['Total Stretcher pts'], mode='markers', name='Hourly Inflow', showlegend=False, line=dict(color='red', width=4)), secondary_y=False)
fig2.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                          ['Total Stretcher pts_yhat_lower'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
fig2.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                          ['Total Stretcher pts_yhat'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
fig2.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                          ['Total Stretcher pts_yhat_upper'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)

total_stretcher_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 - df.iloc[0].ds.hour))) & (
    forecast.ds > df.iloc[0].ds)][['ds', 'Total Stretcher pts_yhat']].rename({'Total Stretcher pts_yhat': 'y'}, axis=1)

fig2.update_yaxes(title_text="Total Stretcher Pts", secondary_y=False)

fig3 = make_subplots(
    specs=[[{"secondary_y": True}]], subplot_titles=['Vertical TBS'])

fig3.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
                          ['Total Vertical TBS'], mode='markers', name='Total Vertical TBS', showlegend=False, line=dict(color='red', width=4)), secondary_y=False)
fig3.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                          ['Total Vertical TBS_yhat_lower'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
fig3.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                          ['Total Vertical TBS_yhat'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
fig3.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
                          ['Total Vertical TBS_yhat_upper'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)

total_stretcher_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 - df.iloc[0].ds.hour))) & (
    forecast.ds > df.iloc[0].ds)][['ds', 'Total Vertical TBS_yhat']].rename({'Total Vertical TBS_yhat': 'y'}, axis=1)

fig3.update_yaxes(title_text="Total", secondary_y=False, range=[0, max(
    df[df.Date == current.Date]['Total Vertical TBS'].max(), todays_forecast['Total Vertical TBS_yhat_upper'].max())+1])


# DESKTOP

if not mobile:

    alerts_col, spacer, subheaders, col1, col2, col3, col4 = st.columns([
                                                                        3, 1, 2, 2, 2, 2, 2])

    with alerts_col:

        st.subheader('Alerts')

        alert_section = st.empty()

        current_forecast = forecast.set_index('ds').loc[current_ds]

        current_alerts = []

        for column in alert_type_select:
            if column in ['Date', 'Time', 'ds']:
                continue
            try:
                if current[column] > current_forecast[column+'_yhat_upper']:
                    current_alerts.append(column + ': ' + str(current[column]) + ' (' +
                                          str(round(current_forecast[column+'_yhat_upper'], 1)) + ')')
            except:
                continue

        if len(current_alerts) > 0:
            # st.write(current_alerts)
            for alert in current_alerts:
                st.write('**• '+alert + '**')
        else:
            with alert_section:
                st.write('**No active alerts**')

        recent_alerts = st.expander('History (last 4 hours)', expanded=False)
        with recent_alerts:
            for lag in [1, 2, 3, 4]:
                target_report = df.iloc[lag]
                target_forecast = forecast.set_index(
                    'ds').loc[target_report.ds]
                st.markdown('**'+str(target_report.ds)+'**')
                for column in alert_type_select:
                    try:
                        if target_report[column] > target_forecast[column+'_yhat_upper']:
                            st.write('• '+column + ': ' + str(target_report[column]) + ' (' +
                                     str(round(target_forecast[column+'_yhat_upper'], 1)) + ')')
                    except:
                        continue
    with subheaders:
        st.subheader('Inflow')
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

    with subheaders:
        st.subheader(' ')
        st.subheader(' ')
        st.subheader('Outflow')
    with col1:
        st.metric(label="Admission Requests", value=current['Adm. requests cum'],
                  delta=int(current['Adm. requests cum']-df.iloc[1]['Adm. requests cum']))

    with col2:
        st.metric(label="Admissions", value=current['Admissions cum'],
                  delta=int(current['Admissions cum']-df.iloc[1]['Admissions cum']))

    with col3:
        st.metric(label="Waiting for Admission", value=current['Pts.waiting for admission CUM'],
                  delta=int(current['Pts.waiting for admission CUM']-df.iloc[1]['Pts.waiting for admission CUM']))
    with col4:
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')

    with subheaders:
        st.subheader(' ')
        st.subheader(' ')
        st.subheader('To Be Seen')
    with col1:
        st.metric(label="Total Pods", value=current['Total Pod TBS'],
                  delta=int(current['Total Pod TBS']-df.iloc[1]['Total Pod TBS']))
    with col2:
        st.metric(label="Green", value=current['Green Pts TBS'],
                  delta=int(current['Green Pts TBS']-df.iloc[1]['Green Pts TBS']))

    with col3:
        st.metric(label="Yellow", value=current['Yellow Pts TBS'],
                  delta=int(current['Yellow Pts TBS']-df.iloc[1]['Yellow Pts TBS']))

    with col4:
        st.metric(label="Orange", value=current['Orange Pts TBS'],
                  delta=int(current['Orange Pts TBS']-df.iloc[1]['Orange Pts TBS']))

    with col1:
        st.metric(label="Total Ambulatory", value=int(current['Total Vertical TBS']),
                  delta=int(current['Total Vertical TBS']-df.iloc[1]['Total Vertical TBS']))
    with col2:
        st.metric(label="Vertical", value=int(current['Stretcher Pts TBS in Vertical']+current['Ambulatory Pts TBS in Vertical']),
                  delta=int((current['Stretcher Pts TBS in Vertical']+current['Ambulatory Pts TBS in Vertical'])-(df.iloc[1]['Stretcher Pts TBS in Vertical']+df.iloc[1]['Ambulatory Pts TBS in Vertical'])))

    with col3:
        st.metric(label="QTrack", value=int(current['QTrack Patients TBS']),
                  delta=int(current['QTrack Patients TBS']-df.iloc[1]['QTrack Patients TBS']))

    with col4:
        st.metric(label="Garage", value=int(current['GARAGE patient TBS']),
                  delta=int(current['GARAGE patient TBS']-df.iloc[1]['GARAGE patient TBS']))

    with subheaders:
        st.subheader(' ')
        st.subheader(' ')
        st.subheader(' ')
        st.subheader(' ')
        st.subheader(' ')
        st.subheader(' ')
        st.subheader('Prepod')

    with col1:
        st.metric(label="Total", value=int(current['Triage hallway pts']),
                  delta=int(current['Triage hallway pts']-df.iloc[1]['Triage hallway pts']))
    with col2:
        st.metric(label="TBS", value=int(current['Triage hallway pts TBS']),
                  delta=int((current['Triage hallway pts TBS'])-(df.iloc[1]['Triage hallway pts TBS'])))

    chart_col1, chart_col2, chart_col3 = st.columns(3)
    with chart_col1:
        st.plotly_chart(fig, use_container_width=True,
                        config={'staticPlot': True}
                        )

    with chart_col2:
        st.plotly_chart(fig2, use_container_width=True,
                        config={'staticPlot': True}
                        )

    with chart_col3:
        st.plotly_chart(fig3, use_container_width=True,
                        config={'staticPlot': True}
                        )

    with chart_col1:
        time_filter = st.selectbox(
            'Time Filter', ['Week', 'Month', '3-Month', 'Year', 'All-Time'], 1)
        time_filter_dict = {"Week": 8, "Month": 32, "3-Month": 94,
                            "Year": 366, 'All-Time': len(daily_visits_df)}
        filtered_daily_visits_df = daily_visits_df[daily_visits_df.ds > (
            pd.to_datetime('today')-datetime.timedelta(days=time_filter_dict[time_filter]))]
        filtered_daily_visits_forecast = daily_visits_forecast[daily_visits_forecast.ds > (
            pd.to_datetime('today')-datetime.timedelta(days=time_filter_dict[time_filter]))]

        fig4 = make_subplots()

        fig4.add_trace(go.Scatter(x=filtered_daily_visits_df.ds, y=filtered_daily_visits_df.y,
                                  mode='markers', name='Daily Visits', showlegend=False, line=dict(color='red', width=4)))

        fig4.add_trace(go.Scatter(x=filtered_daily_visits_forecast.ds, y=filtered_daily_visits_forecast.yhat,
                                  mode='lines', name='Daily Visits', showlegend=False, line=dict(color='blue', width=1)))

        fig4.update_yaxes(title_text="Daily Visits", secondary_y=False)
        st.plotly_chart(fig4, use_container_width=True,
                        config={'staticPlot': True}
                        )


# MOBILE
if mobile:

    st.subheader('Alerts')

    alert_section = st.empty()

    current_forecast = forecast.set_index('ds').loc[current_ds]

    current_alerts = []

    for column in alert_type_select:
        if column in ['Date', 'Time', 'ds']:
            continue
        try:
            if current[column] > current_forecast[column+'_yhat_upper']:
                current_alerts.append(column + ': ' + str(current[column]) + ' (' +
                                      str(round(current_forecast[column+'_yhat_upper'], 1)) + ')')
        except:
            continue

    if len(current_alerts) > 0:
        for alert in current_alerts:
            st.write('**• '+alert+'**')
    else:
        with alert_section:
            st.write('**No active alerts**')

    recent_alerts = st.expander('History (last 4 hours)', expanded=False)
    with recent_alerts:
        for lag in [1, 2, 3, 4]:
            target_report = df.iloc[lag]
            target_forecast = forecast.set_index('ds').loc[target_report.ds]
            st.markdown('**'+str(target_report.ds)+'**')
            for column in alert_type_select:
                try:
                    if target_report[column] > target_forecast[column+'_yhat_upper']:
                        st.write('• '+column + ': ' + str(target_report[column]) + ' (' +
                                 str(round(target_forecast[column+'_yhat_upper'], 1)) + ')')
                except:
                    continue

    st.subheader('Inflow')
    st.write("Total: "+str(current['Total Inflow cum']) +
             ' (+'+str(int(current['Total Inflow hrly']))+')')
    st.write("Stretcher: "+str(current['Stretcher Pts cum']) +
             ' (+'+str(int(current['Stretcher Pts hrly']))+')')
    st.write("Ambulatory: "+str(current['Ambulatory Pts cum']) +
             ' (+'+str(int(current['Ambulatory Pts hrly']))+')')
    st.write("Ambulances: "+str(current['Ambulances cum']) +
             ' (+'+str(int(current['Ambulances hrly']))+')')
    st.subheader('Outflow')

    st.write("Admission Requests: "+str(current['Adm. requests cum'])+' ← '+str(
        int(df.iloc[1]['Adm. requests cum'])))

    st.write("Admissions: "+str(current['Admissions cum'])+' (+' +
             str(int(current['Admissions cum']-df.iloc[1]['Admissions cum']))+')')

    st.write("Waiting for Admission: "+str(current['Pts.waiting for admission CUM'])+' ← ' +
             str(int(df.iloc[1]['Pts.waiting for admission CUM'])))

    st.subheader('To Be Seen')

    st.write("Total Pods: " + str(current['Total Pod TBS'])+' ← ' +
             str(int(df.iloc[1]['Total Pod TBS'])))

    st.write("Green: "+str(current['Green Pts TBS']) +
             ' ← '+str(int(df.iloc[1]['Green Pts TBS'])))

    st.write("Yellow: "+str(current['Yellow Pts TBS']) +
             ' ← '+str(int(df.iloc[1]['Yellow Pts TBS'])))

    st.write("Orange: "+str(current['Orange Pts TBS']) +
             ' ← '+str(int(df.iloc[1]['Orange Pts TBS'])))
    st.write("Total Ambulatory: "+str(int(current['Total Vertical TBS'])) +
             ' ← '+str(int(df.iloc[1]['Total Vertical TBS'])))
    st.write("Vertical: "+str(int(current['Stretcher Pts TBS in Vertical']+current['Ambulatory Pts TBS in Vertical']))+' ← ' +
             str(int((df.iloc[1]['Stretcher Pts TBS in Vertical']+df.iloc[1]['Ambulatory Pts TBS in Vertical']))))

    st.write("QTrack: " + str(int(current['QTrack Patients TBS'])) +
             ' ← ' + str(int(df.iloc[1]['QTrack Patients TBS'])))

    st.write("Garage: " + str(int(current['GARAGE patient TBS']))+' ← ' +
             str(int(df.iloc[1]['GARAGE patient TBS'])))

    st.subheader('Prepod')

    st.write("Total: "+str(int(current['Triage hallway pts']))+' ← ' +
             str(int(current['Triage hallway pts']-df.iloc[1]['Triage hallway pts'])))

    st.write("TBS: "+str(int(current['Triage hallway pts TBS']))+' ← ' +
             str(int(current['Triage hallway pts TBS']-df.iloc[1]['Triage hallway pts TBS'])))

    today = df.iloc[0].ds.date()

    todays_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 -
                                                                                   df.iloc[0].ds.hour))) & (forecast.ds > (df.iloc[0].ds + datetime.timedelta(hours=-1 -
                                                                                                                                                              df.iloc[0].ds.hour)))]

    # fig = make_subplots(specs=[[{"secondary_y": True}]])

    # fig.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
    #                          ['Total Inflow hrly'], mode='markers', name='Hourly Inflow', showlegend=False, line=dict(color='red', width=4)), secondary_y=False)
    # fig.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                          ['Total Inflow hrly_yhat_lower'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
    # fig.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                          ['Total Inflow hrly_yhat'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
    # fig.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                          ['Total Inflow hrly_yhat_upper'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)

    # fig.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
    #                          ['Total Inflow cum'], mode='lines', name='Total Inflow', showlegend=False, line=dict(color='blue', width=4)), secondary_y=True)

    # total_inflow_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 -
    #                                                                                      df.iloc[0].ds.hour))) & (forecast.ds > df.iloc[0].ds)][['ds', 'Total Inflow hrly_yhat']]

    # total_inflow_forecast['y'] = total_inflow_forecast['Total Inflow hrly_yhat'].astype(
    #     int).expanding().sum().astype(int).add(df.iloc[0]['Total Inflow cum'])

    # total_inflow_forecast = pd.concat([df.head(1)[['ds', 'Total Inflow cum']].rename(
    #     {'Total Inflow cum': 'y'}, axis=1), total_inflow_forecast])

    # fig.add_trace(go.Scatter(x=total_inflow_forecast.ds, y=total_inflow_forecast.y, mode='lines',
    #                          name='Total Inflow (expected)', showlegend=False, line=dict(color='blue', width=1, dash='dot')), secondary_y=True)

    # fig.update_yaxes(title_text="Hourly Inflow", secondary_y=False)
    # fig.update_yaxes(title_text="Total Inflow", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True,
                    config={'staticPlot': True}
                    )

    # fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # fig2.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
    #                           ['Total Stretcher pts'], mode='markers', name='Hourly Inflow', showlegend=False, line=dict(color='red', width=4)), secondary_y=False)
    # fig2.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                           ['Total Stretcher pts_yhat_lower'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
    # fig2.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                           ['Total Stretcher pts_yhat'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
    # fig2.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                           ['Total Stretcher pts_yhat_upper'], mode='lines', name='Hourly Inflow (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)

    # total_stretcher_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 - df.iloc[0].ds.hour))) & (
    #     forecast.ds > df.iloc[0].ds)][['ds', 'Total Stretcher pts_yhat']].rename({'Total Stretcher pts_yhat': 'y'}, axis=1)

    # fig2.update_yaxes(title_text="Total Stretcher Pts", secondary_y=False)

    st.plotly_chart(fig2, use_container_width=True,
                    config={'staticPlot': True}
                    )

    # fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    # fig3.add_trace(go.Scatter(x=df.ds, y=df[df.Date == current.Date]
    #                           ['Total Vertical TBS'], mode='markers', name='Total Vertical TBS', showlegend=False, line=dict(color='red', width=4)), secondary_y=False)
    # fig3.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                           ['Total Vertical TBS_yhat_lower'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
    # fig3.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                           ['Total Vertical TBS_yhat'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)
    # fig3.add_trace(go.Scatter(x=todays_forecast.ds, y=todays_forecast
    #                           ['Total Vertical TBS_yhat_upper'], mode='lines', name='Total Vertical TBS (expected)', showlegend=False, line=dict(color='red', width=1, dash='dot')), secondary_y=False)

    # total_stretcher_forecast = forecast[(forecast.ds <= (df.iloc[0].ds + datetime.timedelta(hours=24 - df.iloc[0].ds.hour))) & (
    #     forecast.ds > df.iloc[0].ds)][['ds', 'Total Vertical TBS_yhat']].rename({'Total Vertical TBS_yhat': 'y'}, axis=1)

    # fig3.update_yaxes(title_text="Total Vertical TBS", secondary_y=False)

    st.plotly_chart(fig3, use_container_width=True,
                    config={'staticPlot': True}
                    )

    time_filter = st.selectbox(
        'Time Filter', ['Week', 'Month', 'Year', 'All-Time'], 1)
    time_filter_dict = {"Week": 8, "Month": 32,
                        "Year": 366, 'All-Time': len(daily_visits_df)}
    filtered_daily_visits_df = daily_visits_df[daily_visits_df.ds > (
        pd.to_datetime('today')-datetime.timedelta(days=time_filter_dict[time_filter]))]

    fig4 = make_subplots()

    fig4.add_trace(go.Scatter(x=filtered_daily_visits_df.ds, y=filtered_daily_visits_df .y,
                              mode='markers', name='Daily Visits', showlegend=False, line=dict(color='red', width=4)))

    fig4.update_yaxes(title_text="Daily Visits", secondary_y=False)
    st.plotly_chart(fig4, use_container_width=True,
                    config={'staticPlot': True}
                    )
