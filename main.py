import streamlit as st
from src import extract

st.set_page_config(
    page_title="Echodb",
    page_icon="📡",
    layout="wide")

extract.get_token()
