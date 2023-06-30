import streamlit as st
import streamlit.components.v1 as components
from src.utils import *

# TODO: APP SETUP
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
"""
# TODO: LOGS
st.markdown("##")
l, r = st.columns([1.5, 1])
with l:
    tracks, artists = get_timeline("data/logs.log")
    fig = graph_timeline(tracks, artists)
    st.plotly_chart(fig, True)


with r:
    st.subheader("[Date]: `2023-06-20`")
    with open("data/logs.log") as f:
        for line in f.readlines():
            line = line.replace("INFO", ":pencil:")
            line = line.replace("WARNING", ":warning:")
            st.markdown(line)

a = pd.read_csv("data/artists.csv")
t = pd.read_csv("data/tracks.csv")
# TODO: MEDIA IFRAME
with st.container():
    tracks, artists = get_timeline("data/logs.log")
    infos = pd.read_csv("data/playlist.csv").to_dict(orient="records")

    l, m, r = st.columns([1, 1, 1])
    with l:
        fig = graph_portion(len(t), len(a))
        st.plotly_chart(fig, True)

    with m:
        st.subheader("Extract details")
        tabl, tabm, tabr = st.tabs(
            ["Discovery Weekly", "Release Radar", "Pop Rising"])
        with tabl:
            components.iframe(f"https://open.spotify.com/embed/playlist/{infos[0]['playlist_id']}?utm_source=generator",
                              height=160)
        with tabm:
            components.iframe(f"https://open.spotify.com/embed/playlist/{infos[1]['playlist_id']}?utm_source=generator",
                              height=160)
        with tabr:
            components.iframe(f"https://open.spotify.com/embed/playlist/{infos[2]['playlist_id']}?utm_source=generator",
                              height=160)
        st.markdown(f"**Tracks**: {len(t)} new tracks")
        st.markdown(f"**Artists**: {len(a)} new artists")
        st.markdown(f"**Timelapse**: `{calc_timelapse('data/logs.log')}`")

    with r:
        fig = graph_sunburst()
        st.plotly_chart(fig, True)


# TODO: ARTIST VIEW
st.write("##")
l, r = st.columns([1, 3])
view = a
with l:
    st.header("Artist View")
    st.write(view.describe())
    st.write(f"`Records`: {len(view)}")
    st.write(f"`Author`: Nauqh")
with r:
    st.dataframe(filter_dataframe(view), hide_index=True)
    st.download_button(
        label="Download as csv",
        data=convert_df(view),
        file_name='artists.csv',
        mime='text/csv',
    )

# TODO: TRACK VIEW
st.write("##")
st.header("Track View")
view = t
st.dataframe(filter_dataframe(view), hide_index=True)
st.download_button(
    label="Download as csv",
    data=convert_df(view),
    file_name='tracks.csv',
    mime='text/csv',
)
