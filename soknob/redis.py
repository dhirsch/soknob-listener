import json
import redis
from soknob.config import get_settings
from soknob.exceptions import MissingOrInvalidToken

import logging
logger = logging.getLogger()

# Constants used for naming keys
SONOS_TOKEN = "soknob:sonos_api_token"
SONOS_API_KEY = "soknob:sonos_api_key"
SONOS_API_SECRET = "soknob:sonos_api_secret"
PRIMARY_GROUP = "soknob:primary_group"

def get_redis() -> redis.Redis:
    settings = get_settings()
    return redis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True
    )

def get_token() -> dict:
    """Retrieves the token from Redit and deserializes"""
    rc = get_redis()
    token_string = rc.get(SONOS_TOKEN)
    if not token_string:
        raise MissingOrInvalidToken()
    logger.debug("Returning token string")
    return json.loads(token_string)

def save_token(obj):
    rc = get_redis()
    token_string = json.dumps(obj)
    rc.set(SONOS_TOKEN, token_string)
    logger.debug("Saving token string")
