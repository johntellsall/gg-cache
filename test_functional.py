import random

def make_random():
    return str(random.randint(10000, 99999))

def test_health(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'{"redis":true,"status":"up"}\n' == response.data

# TODO reset database after each test
def test_setget(test_client):
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
    keys = [make_random(), make_random()]
    response = test_client.get(f'/mget/' + ','.join(keys))
    assert response.status_code == 200
    assert response.json == {'value': [None, None]}

def test_mget(test_client):
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
