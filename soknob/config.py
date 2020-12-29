from typing import List

household: str = "Sonos_q39mZheHgt8zLMlNYsAGRnmvac.ESsxhPXK2_Y-WEmTOpTY"
main_player: str = "RINCON_7828CA5F21C001400"
inside_players: List[str] = [
    "RINCON_7828CA5F21C001400",
    "RINCON_7828CAEA8F7401400",
    "RINCON_347E5C1E428801400",
    "RINCON_48A6B87054C401400",
]
volume_up_delta: int = 3
volume_down_delta: int = -3
techno_playlist_id: str = "1"
redis_host: str = "localhost"
redis_port: int = 6379
sonos_api_url = "https://api.ws.sonos.com/control/api/v1"
sonos_api_refresh_url = "https://api.sonos.com/login/v3/oauth/access"
primary_group_ttl = 60 * 10  # 10 minutes
udp_port = 4998
