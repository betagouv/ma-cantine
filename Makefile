DOCKER-RUN = docker compose run -e TERM --rm --entrypoint=""

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

sh:
	$(DOCKER-RUN) server bash

static:
	$(DOCKER-RUN) server python manage.py collectstatic --no-input
