DOCKER-RUN = docker compose run -e TERM --rm --entrypoint=""

.PHONY: build build-server up down sh static

build:
	docker compose build

build-server:
	docker compose -f 'compose.yaml' up -d --build 'server'

up:
	docker compose up

down:
	docker compose down

sh:
	$(DOCKER-RUN) server bash

static:
	$(DOCKER-RUN) server python manage.py collectstatic --no-input
