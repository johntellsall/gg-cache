all: build run

build dc-build:
	docker-compose build

dc-run:  dc-build
	docker-compose run --service caching-service python3 server.py

dc-shell: dc-build
	docker-compose run --service caching-service bash

test: dc-build
	docker-compose run caching-service pytest

# build:
# 	docker build -t caching-service .
# run:
# 	docker run redis:3.2-alpine
# 	docker run caching-service

# redis:
# 	docker run -d -p 6379 redis:3.2-alpine


# setup:
# 	cat < /dev/null > .env
# 	echo REDIS_URL= >> .env
# run:
# 	docker run --name my-redis -d redis
# 	docker run --link my-redis:redis \
# 	caching-service
