# gg-cache

This project is a simple caching app, with a REST API, backed by Redis.

# Quick Overview

This project allows the caller to set and get strings via a REST interface. 

To play around with it, it's running in Heroku here:

https://gg-cache.herokuapp.com/

A minimal example follows. We can 0) make sure the service is up, 1) set a string value given a string key, and 2) fetch the value.

```
$ curl https://gg-cache.herokuapp.com/
{
  "redis": true,
  "status": "up"
}
$ curl -XPOST  --data '{"value":"tasty"}' http://gg-cache.herokuapp.com/set/beer
{
  "code": 200
}
$ curl https://gg-cache.herokuapp.com/get/beer
{
  "value": "tasty"
}
```

For more info, see the specification in the Resources.

# Testing

For a quick rebuild and test, type `make test`

To build and run the project locally, then run verbose tests, type `make testv`

```
$ make testv
...
=========================== test session starts ===========================
platform linux -- Python 3.6.7, pytest-4.5.0, py-1.8.0, pluggy-0.11.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /code
collected 4 items

test_functional.py::test_health PASSED                              [ 25%]
test_functional.py::test_setget PASSED                              [ 50%]
test_functional.py::test_mget_no_values PASSED                      [ 75%]
test_functional.py::test_mget PASSED                                [100%]

======================== 4 passed in 0.14 seconds =========================
```

# Development

There are a number of good tools in the `Makefile`, see that for more information. Each verb is documented. 

## run locally

To run the server locally using Docker, type `make run`

```
$ make run

Starting gg-cache_redis_1 ... done
[2019-05-28 14:54:27,576] INFO in server: Config: {'REDIS_URL': 'redis://redis', 'SERVER_PORT': None, 'PORT': None}
[2019-05-28 14:54:27,576] INFO in server: Redis: redis://redis
[2019-05-28 14:54:27,579] INFO in server: starting: port=5000
 * Serving Flask app "server" (lazy loading)
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
[2019-05-28 14:54:27,811] INFO in server: Config: {'REDIS_URL': 'redis://redis', 'SERVER_PORT': None, 'PORT': None}
[2019-05-28 14:54:27,811] INFO in server: Redis: redis://redis
[2019-05-28 14:54:27,815] INFO in server: starting: port=5000

```

The webapp is now accessible via the host port 5000, testable using good old Curl:

```
$ curl localhost:5000
{
  "redis": true,
  "status": "up"
}
```

## develop inside container

To create a local environment, type `make shell`. This starts a private Redis instance, sets up another container for the webapp, and starts a Bash shell inside the webapp container. The host volume is mapped in to the container, to support development. A dev can make changes using Vscode or another editor, and see the results immediately reflected by running `pytest` or other tools inside the container.

```
$ make shell
...
ggcache@e9a305b2e789:/code$ ls
Dockerfile  README.md    dist                server.py
Makefile    __pycache__  docker-compose.yml  test_functional.py
Procfile    conftest.py  requirements.txt
ggcache@e9a305b2e789:/code$ pytest
=========================== test session starts ===========================
platform linux -- Python 3.6.7, pytest-4.5.0, py-1.8.0, pluggy-0.11.0
rootdir: /code
collected 4 items

test_functional.py ....                                             [100%]

======================== 4 passed in 0.15 seconds =========================
ggcache@e9a305b2e789:/code$
```

# Continuous Integration

The project works with the Drone.io service to support Continuous Integration. To push local updates to CI:

(if on "master" branch):

    $ git push

Currently Drone builds the Docker image, and pushes it to DockerHub. To see Drone in action:

https://cloud.drone.io/johntellsall/gg-cache/


# Deployment

To deploy to the default environment (Heroku), type "make deploy". It expects a valid key to be in the `HEROKU_API_KEY` environment variable.  Example:

    # do this once per session:
    export HEROKU_API_KEY=$(heroku authorizations:create --short)
    
    make deploy




# Resources

## Project Specification

See `devops-engineer-project 2-1.pdf`

## Files

```
.drone.yml      config for Drone.io CI
.gitignore      ignore files from Git
Dockerfile      config Cache webapp Docker container
Makefile        **main file** with dev tools
Procfile        Heroku: run Cache webapp
README.md       this file
conftest.py     dev testing config
docker-compose.yml  local Docker dev/test
requirements.txt    Python modules needed by webapp
server.py       webapp service source code
test_functional.py  API-level tests
```

# Author

* John Mitchell - https://twitter.com/JohnTellsAll

