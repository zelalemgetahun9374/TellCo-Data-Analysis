import numpy as np
import pandas as pd
import pandas_profiling
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title="Tellco Data", layout="wide")

# cache the result so that it doesn't load everytime
@st.cache()
def loadData():
    df = pd.read_csv('data/clean_data.csv')
    return df

def displayData(df):
    st.sidebar.title("Filter tellco data")
    # hashTags = st.sidebar.multiselect("Choose hashtags", list_of_hashtags(df))
    # location = st.sidebar.multiselect("Choose location of tweets", list(df['place'].unique()))
    # source = st.sidebar.multiselect("Choose source of tweets", list(df['source'].unique()))
    # language = st.sidebar.multiselect("Choose language of tweets", list(df['language'].unique()))

    # st.write("Filter the data to your specification. To order the data by a certain column click on the name of the column.")
    # if hashTags:
    #     df = df[df["hashtags"].str.contains('|'.join(hashTags))].reset_index(drop=True)
    # if location:
    #     df = df[np.isin(df, location).any(axis=1)].reset_index(drop=True)
    # if source:
    #     df = df[np.isin(df, source).any(axis=1)].reset_index(drop=True)
    # if language:
    #     df = df[np.isin(df, language).any(axis=1)].reset_index(drop=True)

    st.write(df)


def selectHashTag(df):
    hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)


def advanced_exploration(df, suppress_st_warning=True):
    df = df.drop(columns=["Bearer Id"])
    pr = df.profile_report(explorative=True)
    st_profile_report(pr)


def plotly_bar_sentiment_friends(df):
    st.markdown("## 1. Sentiment vs Friends count")
    st.write("The following bar chart shows the number of friends based on the sentiment of each tweet.")
    fig = px.bar(df, x='sentiment', y='friends_count', color="possibly_sensitive", barmode='group', width=1000)
    st.plotly_chart(fig)

def plotly_bar_original_author_retweet(df):
    count = list(df["original_author"].value_counts().head(10).index)
    df = df[np.isin(df, count).any(axis=1)]
    st.markdown("## 3. Original authors vs Retweet count")
    st.write("The following bar chart shows the number of retweets for the top 10 original authors. Here we can understand that even if PuneUpdater is the highest original author of all, he has very few retweets.")
    fig = px.bar(df, x='original_author', y='retweet_count', color="sentiment", barmode='group', width=1000)
    st.plotly_chart(fig)

def plotly_bar_source_retweet(df):
    count = list(df["source"].value_counts().head(5).index)
    df = df[np.isin(df, count).any(axis=1)]
    st.markdown("## 4. Source vs Retweet count")
    st.write("The following bar chart shows the number of retweets for the top 5 sources.")
    fig = px.bar(df, x='source', y='retweet_count', color="sentiment", barmode='group', width=1000)
    st.plotly_chart(fig)

def plotly_facet(df):
    source = list(df["source"].value_counts().head(3).index)
    df = df[np.isin(df, source).any(axis=1)]
    fig = px.bar(df, x="sentiment", y="friends_count",
             facet_row="possibly_sensitive", facet_col="source", width=1000, height=600)
    st.markdown("## 5. Sentiment vs Retweet count vs Source vs Possibly sensitive")
    st.write("The following faceted subplots show the number of friends based on sentiments and sensetiveness for the top 3 sources grouped .")
    st.plotly_chart(fig)

def authorPie(df):
    dflocationCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['clean_text'].count()}).reset_index()
    dflocationCount = dflocationCount.sort_values("Tweet_count", ascending=False)
    dflocationCount.loc[dflocationCount['Tweet_count'] < 5, 'original_author'] = 'Other authors'
    fig = px.pie(dflocationCount, values='Tweet_count', names='original_author', width=800, height=500)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.markdown("## 2. Original authors")
    st.write("The following pie chart shows top original authors based on their count of tweets. Note that authors with less than 5 tweets are grouped as other authors.")
    st.plotly_chart(fig)

# because the data in the database doesn't change, we need to call loadData() only once
df = loadData()
st.sidebar.title("Pages")
choices = ["Data table", "Advanced data exploration"]
page = st.sidebar.selectbox("Choose Page",choices)

if page == "Data table":
    st.title("Data")
    st.write("\n")
    displayData(df)
# elif page == "WordCloud":
#     wordCloud(df)
# elif page == "Charts":
#     st.title("Charts")
#     plotly_bar_sentiment_friends(df)
#     authorPie(df)
#     plotly_bar_original_author_retweet(df)
#     plotly_bar_source_retweet(df)
#     plotly_facet(df)
else:
    advanced_exploration(df)
st.write('Tellco Data Analysis')