import simplejson as json

CONFIG_FILENAME = 'sonos.json'

def get_config():
    try:
        with open(CONFIG_FILENAME, 'r') as fp:
            return json.load(fp)
    except:
        return {}


def save_config(obj):
    with open(CONFIG_FILENAME, 'w') as fp:
        json.dump(obj, fp)
