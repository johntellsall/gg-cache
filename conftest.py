import pytest

import server # XXXX check this

@pytest.fixture(scope='module')
def test_client():
    if 0:
        flask_app = create_app('flask_test.cfg')
    else:
        flask_app = server.app

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
