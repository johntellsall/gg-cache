# test_functional.py -- do API-level tests
#
# Note: avoid using simple "0"/"1" values in tests, it's too easy to have off-by-one errors, or check state accidentally left from a previous run.

import random

def make_random():
    return str(random.randint(10000, 99999))

def test_health(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is correct
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'{"redis":true,"status":"up"}\n' == response.data

def test_setget(test_client):
    "check key missing (404), set it, check the value now correct"
    key = make_random()
    value = make_random()

    response = test_client.get(f'/get/{key}')
    assert response.status_code == 404

    response = test_client.post(f'/set/{key}', json={'value': value})
    assert response.status_code == 200

    response = test_client.get(f'/get/{key}')
    assert response.status_code == 200
    assert response.json == {'value': value}

def test_mget_no_values(test_client):
    "verify mget returns list of Nones, not 404"
    keys = [make_random(), make_random()]
    response = test_client.get(f'/mget/' + ','.join(keys))
    assert response.status_code == 200
    assert response.json == {'value': [None, None]}

def test_mget(test_client):
    "set multiple values, verify single-call mget fetches them"
    keys = [make_random(), make_random()]
    # TODO regenerate if keys same
    values = [make_random(), make_random()]

    response = test_client.post(f'/set/{keys[0]}', json={'value': values[0]})
    assert response.status_code == 200
    response = test_client.post(f'/set/{keys[1]}', json={'value': values[1]})
    assert response.status_code == 200

    response = test_client.get(f'/mget/' + ','.join(keys))
    assert response.status_code == 200
    assert response.json == {'value': values}
