import pytest

import server

@pytest.fixture(scope='function')
def test_client():
    flask_app = server.app

    testing_client = flask_app.test_client()

    # create a clean App
    ctx = flask_app.app_context()
    ctx.push()
    # zap all state (e.g. Redis)
    server.redis.flushall()

    yield testing_client

    ctx.pop()
