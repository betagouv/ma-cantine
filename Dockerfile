# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.11
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim as base

# Install the project into `/app`
WORKDIR /app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Fix error : failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# in order to download the magic auth dependency, which comes from a github repo
# we need to install git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git libpq-dev gcc npm

# i had a problem accessing github.com. When I followed https://docs.docker.com/desktop/get-started/#credentials-management-for-linux-users
# and restarted the problem was resolved

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev


# Copy the source code into the container.
COPY . .

# Installing separately from its dependencies allows optimal layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Copy again source code after installing projet dependencies
COPY . .

# Switch to the non-privileged user to run the application.
USER appuser

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Expose the port that the application listens on.
EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
