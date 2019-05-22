all: build run

run-simple: killall
	docker build -t caching-service .
	docker run -p 5000:5000 caching-service

# TODO
run: killall

killall:
	docker-compose down
	docker ps -q | xargs −−no−run−if−empty docker kill

build dc-build:
	docker-compose build

dc-run:  dc-build
	docker-compose run --service caching-service python3 server.py

dc-shell: dc-build
	docker-compose run --service caching-service bash

test: dc-build
	docker-compose run caching-service pytest

deploy: d-heroku

HEROKU_APP=gg-cache
HEROKU_PROCESS_TYPE=web
d-heroku:
	# login to Heroku's registry w/ given token 
	docker login --username=_ --password=${HEROKU_API_KEY} registry.heroku.com
	# push locally-built image to Heroku registry
	docker tag gg-cache_caching-service registry.heroku.com/${HEROKU_APP}/${HEROKU_PROCESS_TYPE}
	docker push registry.heroku.com/${HEROKU_APP}/${HEROKU_PROCESS_TYPE}
	heroku container:release web --verbose
	
# build image locally, then push to Heroku registry
# (doesn't require token)
deploy-simple:
	heroku container:push web
	heroku container:release web --verbose


# redis:
# 	docker run -d -p 6379 redis:3.2-alpine


# setup:
# 	cat < /dev/null > .env
# 	echo REDIS_URL= >> .env
# run:
# 	docker run --name my-redis -d redis
# 	docker run --link my-redis:redis \
# 	caching-service
