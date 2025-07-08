DOCKER-RUN = docker compose run -e TERM --rm --entrypoint=""

.PHONY: runserver shell shell_plus docker-build docker-build-server docker-up docker-down docker-compose-sh docker-compose-collectstatic

# Local
runserver:
	python manage.py runserver

shell:
	python manage.py shell

shell_plus:
	python manage.py shell_plus

# Docker
docker-build:
	docker compose build

docker-build-server:
	docker compose -f 'compose.yaml' up -d --build 'server'

docker-up:
	docker compose up

docker-down:
	docker compose down

docker-compose-sh:
	$(DOCKER-RUN) server bash

docker-compose-collectstatic:
	$(DOCKER-RUN) server python manage.py collectstatic --no-input
