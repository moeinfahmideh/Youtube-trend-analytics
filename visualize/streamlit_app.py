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

st.title("YouTube Analytics Dashboard")

tab1, tab2 = st.tabs(["Top Videos", "Channel Summary"])

with tab1:
    df_vid = load_data("SELECT * FROM clean.video_snapshot ORDER BY view_count DESC LIMIT 20;")
    st.dataframe(df_vid)

with tab2:
    df_chn = load_data("SELECT * FROM clean.channel_summary ORDER BY total_views DESC LIMIT 20;")
    st.dataframe(df_chn)
