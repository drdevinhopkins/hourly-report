import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly as py


st.title("Hourly Report")

df = pd.read_csv('../data/recent-clean.csv')

df = df.set_index('ds').head(72)

st.write(df.head(5))

current = df.iloc[0]

st.header('Inflow')

st.subheader('Today')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Stretcher", value=df['Stretcher Pts cum'].tolist()[0],
              delta=df['Stretcher Pts cum'].tolist()[0]-df['Stretcher Pts cum'].tolist()[1])
with col2:
    st.metric(label="Ambulatory", value=df['Ambulatory Pts cum'].tolist()[0],
              delta=df['Ambulatory Pts cum'].tolist()[0]-df['Ambulatory Pts cum'].tolist()[1])
with col3:
    st.metric(label="Total", value=df['Total Inflow cum'].tolist()[0],
              delta=df['Total Inflow cum'].tolist()[0]-df['Total Inflow cum'].tolist()[1])

fig = go.Figure()
# fig.update_layout(title_text="Inflow",
#                   title_font_size=18)
fig.add_trace(go.Scatter(x=df.index, y=df['Total Inflow hrly'], mode='lines',
                         name='Total Inflow', showlegend=True))
fig.add_trace(go.Scatter(x=df.index, y=df['Stretcher Pts hrly'], mode='lines',
                         name='Stretcher Inflow', showlegend=True))
fig.add_trace(go.Scatter(x=df.index, y=df['Ambulatory Pts hrly'], mode='lines',
                         name='Stretcher Inflow', showlegend=True))
st.plotly_chart(fig)
