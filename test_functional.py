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
    assert 0, response
    assert response.status_code == 404
