import functools
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import requests
import time

import storage

API_URL = "https://api.ws.sonos.com/control/api/v1"

config = storage.get_config()
client = OAuth2Session(client_id=config['API_KEY'], token=config['token'])
client.headers['Content-Type'] = 'application/json'

def sonos_oauth_refresh_client():
    config = storage.get_config()
    token = config.get('token')
    if not token:
        raise Exception("Missing configuration")
    if 'expires_at' in token:
        token['expires_in'] = int(token['expires_at'] - time.time())
    client = OAuth2Session(
        client_id=config['API_KEY'],
        scope=['playback-control-all'],
        auto_refresh_url='https://api.sonos.com/login/v3/oauth/access',
        token_updater=save_token_data,
        token=token
    )
    client.headers['Content-Type'] = 'application/json'
    return client


def refresh_token():
    print('Refreshing token')
    token = client.refresh_token(
        'https://api.sonos.com/login/v3/oauth/access',
        refresh_token=config['token']['refresh_token'],
        auth=(config['API_KEY'], config['API_SECRET'])
    )
    print(token)
    save_token_data(token)
    client.token = token


def save_token_data(token):
    config = storage.get_config()
    config['token'] = token
    storage.save_config(config)

def auto_refresh_token(func):
    @functools.wraps(func)
    def wrapper_auto_refresh_token(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TokenExpiredError:
            refresh_token()
            return func(*args, **kwargs)
    return wrapper_auto_refresh_token


@auto_refresh_token
def get_groups():
    config = storage.get_config()
    household = config['household']
    url = f"{API_URL}/households/{household}/groups"
    resp = client.get(url)
    print(resp.json())
    return resp.json()


@auto_refresh_token
def find_primary_group():
    groups = get_groups()
    primary = config['main_player']
    for group in groups.get('groups', []):
        if primary in group['playerIds']:
            return group['id']


@auto_refresh_token
def group_volume_delta(group_id: str, delta: int):
    url = f"{API_URL}/groups/{group_id}/groupVolume/relative"
    return client.post(url, json={"volumeDelta": delta}).json()


@auto_refresh_token
def start_playlist(group_id: str, playlist_id: str, shuffle: bool = True, repeat: bool = False):
    url = f"{API_URL}/groups/{group_id}/playlists"
    body = {
        "action": "replace",
        "playlistId": playlist_id,
        "playOnCompletion": True,
        "playModes": {
            "shuffle": shuffle,
            "repeat": repeat,
        }
    }
    return client.post(url, json=body).json()


@auto_refresh_token
def make_group():
    config = storage.get_config()
    household = config['household']
    players = config['inside_players']
    url = f'{API_URL}/households/{household}/groups/createGroup'
    body = {
        'playerIds': players
    }
    resp = client.post(url, json=body).json()
    group_id = resp.get('groups', {}).get('id')

    for player in players:
        url = f'{API_URL}/players/{player}/playerVolume'
        client.post(url, json={'volume': 30, 'muted': False})

    # volume_url = f'{API_URL}/groups/{group_id}/groupVolume'
    # volume_body = {
    #     'volume': 30
    # }
    # client.post(volume_url, json=volume_body)
    return group_id