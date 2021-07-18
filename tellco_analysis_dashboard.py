import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Tellco Data", layout="wide")

# cache the result so that it doesn't load everytime
@st.cache()
def loadData():
    df = pd.read_csv('data/clean_data.csv')
    df['Total Avg RTT (ms)'] = df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']
    df['Total Avg Bearer TP (kbps)'] = df['Avg Bearer TP DL (kbps)'] + df['Avg Bearer TP UL (kbps)']
    df['Total TCP Retrans. Vol (Bytes)'] = df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)']

    df = df[[
        'Bearer Id',
        'Dur (ms)',
        'IMSI',
        'MSISDN/Number',
        'IMEI',
        'Total Avg RTT (ms)',
        'Total Avg Bearer TP (kbps)',
        'Total TCP Retrans. Vol (Bytes)',
        'Handset Manufacturer',
        'Handset Type',
        'Social Media Data Volume (Bytes)',
        'Google Data Volume (Bytes)',
        'Email Data Volume (Bytes)',
        'Youtube Data Volume (Bytes)',
        'Netflix Data Volume (Bytes)',
        'Gaming Data Volume (Bytes)',
        'Other Data Volume (Bytes)',
        'Total Data Volume (Bytes)']]

    scores_df = pd.read_csv('data/user_scores.csv')
    return df, scores_df

def displayHandsetsInfo(df):
    st.title("Users Handsets")
    st.write("")
    st.markdown("**Click the boxes to zoom in and explore all the handset manufacturers and types.**")
    plotly_plot_treemap(df)
    st.write("")
    st.markdown("**Handset manufacturers with more than 200 devices.**")
    plotly_plot_pie(df, 'Handset Manufacturer', 200)
    st.write("")
    st.markdown("**Handset types with more than 700 devices.**")
    plotly_plot_pie(df, 'Handset Type', 700)

def displayClusterInfo(df):
    st.title("User Clusters")
    st.write("")
    st.markdown("**User engagement metrics table**")
    eng_df = df[['MSISDN/Number', 'xDR Sessions', 'Dur (ms)', 'Total Data Volume (Bytes)', 'engagement_score']]
    st.write(eng_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 6 clusters based on their engagement(i.e. number of xDR sessions, duration and total data used).**")
    plotly_plot_scatter(df, 'Total Data Volume (Bytes)', 'Dur (ms)',
            'engagement_cluster', 'xDR Sessions')

    st.write("")
    st.markdown("**User experience metrics table**")
    exp_df = df[['MSISDN/Number', 'Total Avg RTT (ms)',
        'Total Avg Bearer TP (kbps)', 'Total TCP Retrans. Vol (Bytes)', 'experience_score']]
    st.write(exp_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 3 clusters based on their experience(i.e. average RTT, TCP retransmission', and throughput).**")
    plotly_plot_scatter(df, 'Total TCP Retrans. Vol (Bytes)', 'Total Avg Bearer TP (kbps)',
            'experience_cluster', 'Total Avg RTT (ms)')

    st.write("")
    st.markdown("**User satisfaction metrics table**")
    sat_df = df[['MSISDN/Number', 'engagement_score', 'experience_score', 'satisfaction_score']]
    st.write(sat_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 2 clusters based on their satisfactio(i.e. engagement score and experience score).**")
    plotly_plot_scatter(df, 'engagement_score', 'experience_score',
            'satisfaction_cluster', 'satisfaction_score')

def displayApplicationsInfo(df):
    st.title("Usage of applications")
    st.write("")
    st.markdown("**Total data used per application**")
    apps = df[['Social Media Data Volume (Bytes)',
    'Google Data Volume (Bytes)',
    'Email Data Volume (Bytes)',
    'Youtube Data Volume (Bytes)',
    'Netflix Data Volume (Bytes)',
    'Gaming Data Volume (Bytes)',
    'Other Data Volume (Bytes)']].copy(deep=True)
    apps.rename(columns={
        'Social Media Data Volume (Bytes)': 'Social Media',
        'Google Data Volume (Bytes)': 'Google',
        'Email Data Volume (Bytes)': 'Email',
        'Youtube Data Volume (Bytes)': 'Youtube',
        'Netflix Data Volume (Bytes)': 'Netflix',
        'Gaming Data Volume (Bytes)': 'Gaming',
        'Other Data Volume (Bytes)': 'Other'},
        inplace=True)
    total = apps.sum()
    total = total.to_frame('Data volume')
    total.reset_index(inplace=True)
    total.rename(columns={'index': 'Applications'}, inplace=True)
    fig = px.pie(total, names='Applications', values='Data volume')
    st.plotly_chart(fig)
    app_handsets_df = df[[
        'Handset Type',
        'Social Media Data Volume (Bytes)',
        'Google Data Volume (Bytes)',
        'Email Data Volume (Bytes)',
        'Youtube Data Volume (Bytes)',
        'Netflix Data Volume (Bytes)',
        'Gaming Data Volume (Bytes)',
        'Other Data Volume (Bytes)']]
    app_handsets_df = app_handsets_df.groupby('Handset Type').sum()
    sort_df = app_handsets_df.sort_values('Gaming Data Volume (Bytes)').head()


def advanced_exploration(df, suppress_st_warning=True):
    df = df.drop(columns=["Bearer Id"])
    pr = df.profile_report(explorative=True)
    # st_profile_report(pr)

def plotly_plot_pie(df, column, limit=None):
    a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
    a = a.sort_values("count", ascending=False)
    if limit:
        a.loc[a['count'] < limit, column] = f'Other {column}s'
    fig = px.pie(a, values='count', names=column, width=800, height=500)
    st.plotly_chart(fig)

def plotly_plot_treemap(df):
    fig = px.treemap(df, path=[px.Constant("Handset Manufacturers"), 'Handset Manufacturer', 'Handset Type'])
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig)

def plotly_plot_scatter(df, x_col, y_col, color, size):
    fig = px.scatter(scores_df, x=x_col, y=y_col,
                 color=color, size=size)
    st.plotly_chart(fig)

# because the data in the database doesn't change, we need to call loadData() only once
df, scores_df = loadData()
st.sidebar.title("Pages")
choices = ["Handsets", "Applications", "User Clusters"]
page = st.sidebar.selectbox("Choose Page",choices)

if page == "Handsets":
    displayHandsetsInfo(df)
    pass
elif page == "Applications":
    displayApplicationsInfo(df)
elif page == "User Clusters":
    displayClusterInfo(scores_df)
