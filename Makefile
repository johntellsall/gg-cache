# Makefile: develop app locally, or deploy to Heroku

# default -- run webapp (see README.md for how to access)
all: run

# HIGH LEVEL COMMANDS

run: dc-run

test: dc-build
	docker-compose run caching-service -m pytest

deploy: d-heroku


# XX COMMANDS

# run-noredis -- run service alone (no Redis nor Docker-Compose)
run-noredis: killall
	docker build -t caching-service .
	docker run -p 5000:5000 caching-service

# killall -- stop containers listed in docker-compose.yml and stragglers
killall:
	docker-compose down
	docker ps -q | xargs −−no−run−if−empty docker kill

# DOCKER-COMPOSE (DC) COMMANDS

# dc-build -- build images specified in docker-compose.yml
dc-build:
	docker-compose build

# dc-run -- build and run webapp in local terminal
dc-run:  dc-build
	docker-compose run --service caching-service

# dc-shell: dc-build
# 	docker-compose run --service caching-service bash


# DEPLOY (D) COMMANDS

HEROKU_APP=gg-cache
HEROKU_PROCESS_TYPE=web
d-heroku:
	echo "NOTE: create key with 'heroku authorizations:create', put in HEROKU_API_KEY"
	# login to Heroku's registry w/ given token 
	docker login --username=_ --password=${HEROKU_API_KEY} registry.heroku.com
	# push locally-built image to Heroku registry
	docker tag gg-cache_caching-service registry.heroku.com/${HEROKU_APP}/${HEROKU_PROCESS_TYPE}
	docker push registry.heroku.com/${HEROKU_APP}/${HEROKU_PROCESS_TYPE}
	heroku container:release web --verbose
	
# d-simple -- build image locally, push to Heroku registry, deploy via image
# (doesn't require token)
d-simple:
	heroku container:push web
	heroku container:release web --verbose
