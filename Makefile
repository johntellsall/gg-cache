# all: build run


dc-run:
	docker-compose build
	docker-compose run --service caching-service
	
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