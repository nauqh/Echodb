import streamlit as st
from src.extract import *
from src.load import Database
from src.utils import *

# TODO: APP SETUP
db = Database()
st.set_page_config(
    page_title="Echodb",
    page_icon="📡",
    layout="wide")

st.markdown("""<h1 style='
                font-family: Recoleta-Regular; font-weight: 400;
                font-size: 3.5rem'>Echodb</h1>""",
            unsafe_allow_html=True)

st.markdown("""<h3 style='
                font-family: Recoleta-Regular; font-weight: 400;
                font-size: 1.55rem'>Our sophisticated ELT manages your sloppy streaming data</h3>""",
            unsafe_allow_html=True)
"""
![Python](https://img.shields.io/badge/Made%20With-Python%203.11-blue.svg?style=for-the-badge&logo=Python)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)
"""
# TODO:
st.markdown("##")
l, r = st.columns([1.5, 1])
with l:
    ...

with r:
    st.subheader("[Date]: `2023-06-20`")
    with open("data/logs.log") as f:
        for line in f.readlines():
            line = line.replace("INFO", ":pencil:")
            line = line.replace("WARNING", ":warning:")
            st.markdown(line)

# TODO: ARTIST VIEW
st.write("##")
l, r = st.columns([1, 3])
view = db.view("artist")
with l:
    st.header("Artist View")
    st.write(view.describe())
    st.write(f"`Records`: {len(view)}")
    st.write(f"`Author`: Nauqh")
with r:
    st.dataframe(filter_dataframe(view), hide_index=True)

# TODO: TRACK VIEW
st.write("##")
st.header("Track View")
view = db.view("track")
st.dataframe(filter_dataframe(view), hide_index=True)
