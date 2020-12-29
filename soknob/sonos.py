import functools
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import requests
import time

from soknob import config
from soknob import redis

api_url = config.sonos_api_url  # just for convenience

client = OAuth2Session(
    client_id=redis.get_redis().get(redis.SONOS_API_KEY),
    token=redis.get_token()
)
client.headers['Content-Type'] = 'application/json'


def refresh_token():
    print('Refreshing token')
    rc = redis.get_redis()
    token = client.refresh_token(
        config.sonos_api_refresh_url,
        refresh_token=redis.get_token().get('refresh_token'),
        auth=(rc.get(redis.SONOS_API_KEY), rc.get(redis.SONOS_API_SECRET))
    )
    print(token)
    redis.save_token(token)
    client.token = token


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
    household = config.household
    url = f"{api_url}/households/{household}/groups"
    resp = client.get(url)
    return resp.json()


@auto_refresh_token
def find_primary_group():
    rc = redis.get_redis()
    primary_group = rc.get(redis.PRIMARY_GROUP)
    if primary_group:
        print("Using primary group from cache")
        return primary_group

    groups = get_groups()
    primary = config.main_player
    for group in groups.get('groups', []):
        if primary in group['playerIds']:
            primary_group = group['id']
            rc.set(redis.PRIMARY_GROUP, primary_group, ex=config.primary_group_ttl)
            return primary_group
    return None


@auto_refresh_token
def group_volume_delta(group_id: str, delta: int) -> requests.Response:
    url = f"{api_url}/groups/{group_id}/groupVolume/relative"
    return client.post(url, json={"volumeDelta": delta})


@auto_refresh_token
def start_playlist(group_id: str, playlist_id: str, shuffle: bool = True, repeat: bool = False):
    url = f"{api_url}/groups/{group_id}/playlists"
    body = {
        "action": "replace",
        "playlistId": playlist_id,
        "playOnCompletion": True,
        "playModes": {
            "shuffle": shuffle,
            "repeat": repeat,
        }
    }
    return client.post(url, json=body)


@auto_refresh_token
def make_group():
    pass
    # config = storage.get_config()
    # household = config['household']
    # players = config['inside_players']
    # url = f'{API_URL}/households/{household}/groups/createGroup'
    # body = {
    #     'playerIds': players
    # }
    # resp = client.post(url, json=body).json()
    # group_id = resp.get('groups', {}).get('id')

    # for player in players:
    #     url = f'{API_URL}/players/{player}/playerVolume'
    #     client.post(url, json={'volume': 30, 'muted': False})

    # # volume_url = f'{API_URL}/groups/{group_id}/groupVolume'
    # # volume_body = {
    # #     'volume': 30
    # # }
    # # client.post(volume_url, json=volume_body)
    # return group_id