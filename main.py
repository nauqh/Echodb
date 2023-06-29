import streamlit as st
from src.extract import *
from src.load import Database

if __name__ == "__main__":
    db = Database()

    token = get_token()
    print(token)
    urls = get_user_playlists(token)

    for url in urls:
        playlist, artists, tracks = extract_playlist(token, url)
        if playlist != None:
            db.add_playlist(playlist)
            db.add_artists(artists)
            db.add_tracks(tracks)
