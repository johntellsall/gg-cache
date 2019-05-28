# gg-cache

This project is a simple caching app, with a REST API, backed by Redis.

# Quick Overview


https://gg-cache.herokuapp.com/

# Testing

# Development

# Continuous Integration

The project works with the Drone.io service to support Continuous Integration. To push local updates to CI:


# Deployment

To deploy to the default environment (Heroku), type "make deploy". It expects a valid key to be in the `HEROKU_API_KEY` environment variable.  Example:

    $ export HEROKU_API_KEY=$(heroku authorizations:create --short)

    $ make deploy

# Resources

