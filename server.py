# server.py: REST API to store and fetch short string values

import os
from logging.config import dictConfig
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from redis import Redis
from redis import ConnectionError

REDIS_URL = os.getenv("REDIS_URL")

def connect_redis(url):
    redis = Redis.from_url(url)
    return redis

def create_app():
    app = Flask(__name__)
    # TODO: get logging config from external file
    dictConfig({'version': 1, 'root': {'level': 'INFO'}})
    app.logger.info('Config: %s', {
        'REDIS_URL': REDIS_URL, 
        "SERVER_PORT": os.getenv("SERVER_PORT"),
        "PORT": os.getenv("PORT")
    })
    return app

##################
## Global objects: app, redis
##################
redis = connect_redis(REDIS_URL)
app = create_app()

def get_port():
    # PORT is given by Heroku, SERVER_PORT is by specification
    port = os.getenv("SERVER_PORT", os.getenv("PORT", 5000))
    return port

def check_redis():
    try:
        redis.ping()
    except ConnectionError as exc:
        app.logger.error("Redis: can't connect (REDIS_URL=%s)", REDIS_URL)
    except Exception as exc:
        app.logger.critical("Redis: bad error (REDIS_URL=%s)", REDIS_URL)



##################
### Error handling
##################
class ApiException(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(ApiException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

################
### Api endpoint
################
@app.route('/')
def health():
    try:
        redis_status = redis.ping()
        status = "up"
    except ConnectionError as e:
        redis_status = str(e)
        status = "down"
    return jsonify(status=status, redis=redis_status)

@app.route('/get/<key>')
def get(key):
    val = redis.get(key)
    if val is not None:
        val = val.decode('utf-8')
        app.logger.debug(val)
        return jsonify(value=val)
    else:
        raise ApiException(
            message="Could not find key '{}' in cache".format(key),
            status_code=404)

@app.route('/mget/<keys>')
def mget(keys):
    """
    lookup each key, return list of values.
    Keys comma-separated.
    Missing values returned as Nones - this method never gives 404.
    """
    values = redis.mget(keys.split(','))
    values = [val and val.decode('utf-8') for val in values]
    app.logger.debug('mget(%s) = %s', keys, values)
    return jsonify(value=values)

@app.route('/set/<key>', methods=['POST'])
def set(key):
    try:
        payload = request.get_json(force=True)
        if 'value' in payload:
            redis.set(key, payload['value'])
            app.logger.debug(payload['value'])
            return jsonify(code=200)
        else:
            raise ApiException("'value' key not found in JSON payload")
    except ApiException as e:
        raise e
    except Exception as e:
        raise ApiException(str(e))

########
### Main
########
if __name__ == '__main__':
    port = get_port()
    app.logger.info('starting: port=%s', port)
    check_redis()
    app.run(debug=True, host='0.0.0.0', port=port)
