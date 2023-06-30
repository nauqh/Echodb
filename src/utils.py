"""
Utility module for transforming data 
"""

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from datetime import datetime as dt
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import re


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def graph_timeline(tracks: dict, artists: dict):
    df_tracks = pd.DataFrame({'time': list(tracks.keys()),
                              'count': list(tracks.values()),
                              'label': 'tracks'})
    df_artists = pd.DataFrame({'time': list(artists.keys()),
                               'count': list(artists.values()),
                               'label': 'artists'})

    df = pd.merge(df_tracks, df_artists, on='time', how='outer').fillna(0)
    df = df.sort_values('time')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['time'], y=df['count_x'], name='Tracks'))
    fig.add_trace(go.Bar(x=df['time'], y=df['count_y'], name='Artists'))

    fig.update_layout(
        title='Tracks and Artists Timeline',
        xaxis_title='Time',
        yaxis_title='Count'
    )

    fig.update_traces(
        hoverinfo='y', hovertemplate="%{y}")

    return fig


def graph_portion(tracks: int, artists: int):
    labels = ['Playlist', 'Tracks', 'Artists']
    values = [3, tracks, artists]
    colors = ['#b9fbc0', '#98f5e1', '#8eecf5',
              '#90dbf4', '#a3c4f3', '#cfbaf0', 'f1c0e8']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_traces(name='', textfont_size=15,
                      hovertemplate='%{label}: %{value}',
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))

    fig.update_layout(
        title="New records 2023-06-20",
        annotations=[dict(text='Records', x=0.5, y=0.5, font_size=15, showarrow=False)])
    return fig


def graph_sunburst():
    colors = ['#b9fbc0', '#98f5e1', '#8eecf5',
              '#90dbf4', '#a3c4f3', '#cfbaf0', 'f1c0e8']
    fig = go.Figure(go.Sunburst(
        labels=["Spotify", "Rock", "Pop", "R&B",
                "EDM", "Rap", "K-Pop", "Metal", "V-Pop"],
        parents=["", "Spotify", "Spotify", "Spotify",
                 "Spotify", "Spotify", "Pop", "EDM", "Pop"],
        values=[10, 14, 12, 10, 2, 6, 6, 4, 4]
    ))

    fig.update_traces(marker=dict(colors=colors),
                      textfont_color="#000", textfont_size=15)

    fig.update_layout(title={
        'text': "Popular genres (click at Pop, EDM for interaction)",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        margin=dict(t=0, l=0, r=0, b=0))
    return fig


def calc_timelapse(filename: str):
    pattern = r"\[\[(\d+:\d+:\d+)\]\]"

    with open(filename) as f:
        content = f.read()

    matches = re.findall(pattern, content)
    times = [dt.strptime(match, "%H:%M:%S") for match in matches]

    # Calculate time lapse
    return times[-1] - times[0]


def get_timeline(filename: str) -> tuple[dict, dict]:
    tracks = {}
    artists = {}
    pattern = r"\[\[(\d{2}:\d{2}:\d{2})\]\] (?!WARNING).*?Extracted (\d+) (\btracks\b|\bartist\b)"

    with open(filename) as f:
        for line in f.readlines():
            match = re.search(pattern, line)
            if match:
                time = match.group(1)
                number = int(match.group(2))
                item = match.group(3)
                if item == 'tracks':
                    tracks[time] = tracks.get(time, 0) + number
                elif item == 'artist':
                    artists[time] = artists.get(time, 0) + number

        tracks = {dt.strptime(key, "%H:%M:%S").time()                  : value for key, value in tracks.items()}
        artists = {dt.strptime(key, "%H:%M:%S").time()                   : value for key, value in artists.items()}

    return tracks, artists


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], format="/%Y-%m-%d")
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect(
            "**Filter dataframe on**", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(
                        map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(
                        str).str.contains(user_text_input)]

    return df
