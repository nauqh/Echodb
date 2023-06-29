import hydra
import pandas as pd
from tqdm import tqdm
from requests import get
from omegaconf import DictConfig
from spotipy.util import prompt_for_user_token as pm


@hydra.main(version_base=None, config_path="../config", config_name="main")
def get_token(cfg: DictConfig) -> str:
    # token = pm(scope=cfg['spotify']['scope'],
    #            client_id=cfg['spotify']['id'],
    #            client_secret=cfg['spotify']['secret'],
    #            redirect_uri=cfg['spotify']['redirect'])
    print(cfg['spotify']['id'])
    return None


def get_header(token: str):
    return {"Authorization": "Bearer " + token}


def get_playlist(token: str, playlist_url: str) -> dict:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_header(token)

    resp = get(url, headers=headers).json()
    return resp


def get_playlist_info(playlist: dict) -> dict:
    data = {}
    data['id'] = playlist['id']
    data['name'] = playlist['name']
    data['owner'] = playlist['owner']
    data['description'] = playlist['description']
    data['followers'] = playlist['followers']
    data['image'] = playlist['images'][0]['url']
    data['url'] = playlist['external_urls']['spotify']
    return data


def get_track_info(playlist: dict, index: int) -> dict:
    track = playlist['tracks']['items'][index]
    data = {}
    data['name'] = track['track']['name']
    data['added_date'] = track['added_at']
    data['release_date'] = track['track']['album']['release_date']
    data['track_id'] = track['track']['id']
    data['artist_id'] = track['track']['album']['artists'][0]['id']
    data['track_pop'] = track['track']['popularity']
    data['image'] = track['track']['album']['images'][0]['url']
    data['url'] = track['track']['external_urls']['spotify']
    return data


def get_artist_info(token: str, artist_id: str) -> dict:
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_header(token)
    resp = get(url, headers=headers).json()

    artist = {}
    artist['artist_id'] = artist_id
    artist['name'] = resp['name']
    artist['followers'] = resp['followers']['total']
    artist['genres'] = resp['genres']
    artist['popularity'] = resp['popularity']
    if not resp['images']:
        artist['image'] = []
    else:
        artist['image'] = resp['images'][0]['url']
    artist['url'] = resp['external_urls']['spotify']
    return artist


def get_audio_features(token: str, track_id: str) -> dict:
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_header(token)
    resp = get(url, headers=headers).json()

    features = {}
    features['track_id'] = track_id
    features['danceability'] = resp['danceability']
    features['energy'] = resp['energy']
    features['key'] = resp['key']
    features['loudness'] = resp['loudness']
    features['mode'] = resp['mode']
    features['speechiness'] = resp['speechiness']
    features['acousticness'] = resp['acousticness']
    features['instrumentalness'] = resp['instrumentalness']
    features['liveness'] = resp['liveness']
    features['valence'] = resp['valence']
    features['tempo'] = resp['tempo']
    features['duration_ms'] = resp['duration_ms']
    features['time_signature'] = resp['time_signature']
    return features
