import streamlit as st
import psycopg
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from db.connection import get_connection
import pandas as pd

load_dotenv()

@st.cache_data
def load_data(query: str) -> pd.DataFrame:
    with get_connection() as conn:              
        df = pd.read_sql(query, conn)           
    return df


st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")
st.title("🎥 YouTube Analytics Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
date_filter = st.sidebar.date_input("Snapshot Date", [])

# Main tabs
tabs = st.tabs([
    "Video Snapshot",
    "Channel Summary",
    "Viral Index",
    "Underdog Videos",
    "Channel Growth",
])

with tabs[0]:
    st.header("📋 Video Snapshot")
    st.markdown("**What you’ll see**: A real-time leaderboard of the most-viewed videos, with their current view and like counts and when we last fetched them.")
    query = "SELECT * FROM clean.video_snapshot ORDER BY view_count DESC LIMIT 50;"
    df = load_data(query)
    st.dataframe(df)

with tabs[1]:
    st.header("📊 Channel Summary")
    st.markdown("**What you’ll see**: A roll-up of each channel’s performance — total views, total likes, and average views per video, ranked by total views.")
    query = "SELECT * FROM clean.channel_summary ORDER BY total_views DESC LIMIT 50;"
    df = load_data(query)
    st.dataframe(df)

with tabs[2]:
    st.header("🔥 Video Viral Index")
    st.markdown("**What you’ll see**: Videos ranked by their 'viral index', which measures how many views they got relative to their channel’s subscriber count — perfect for spotting underdog hits.")
    query = "SELECT * FROM clean.video_viral_index ORDER BY viral_index DESC LIMIT 50;"
    df = load_data(query)
    st.dataframe(df)

with tabs[3]:
    st.header("🏆 Top Underdog Videos")
    st.markdown("**What you’ll see**: Individual videos that significantly outperformed their channel’s average, identified by a high z-score compared to their channel’s norms.")
    query = "SELECT * FROM clean.underdog_videos ORDER BY z_score DESC LIMIT 50;"
    df = load_data(query)
    st.dataframe(df)

with tabs[4]:
    st.header("🚀 Emerging Channel Growth")
    st.markdown("**What you’ll see**: Channels sorted by their average daily subscriber gains, revealing the fastest-rising stars in your dataset.")
    query = "SELECT * FROM clean.channel_growth ORDER BY avg_daily_gain DESC LIMIT 50;"
    df = load_data(query)
    st.dataframe(df)



# Footer
st.markdown("---")
st.caption("Data sourced from YouTube Data API | Updated daily via scheduled pipeline")
