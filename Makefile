all: build run

build:
	docker build -t caching-service .
run:
	docker run caching-service