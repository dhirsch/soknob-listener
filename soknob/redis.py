import json
import redis
from soknob import config
from soknob.exceptions import MissingOrInvalidToken
from loguru import logger

# Constants used for naming keys
SONOS_TOKEN = "soknob:sonos_api_token"
SONOS_API_KEY = "soknob:sonos_api_key"
SONOS_API_SECRET = "soknob:sonos_api_secret"
PRIMARY_GROUP = "soknob:primary_group"

def get_redis() -> redis.Redis:
    return redis.Redis(
        host=config.redis_host, port=config.redis_port, db=0, decode_responses=True
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
