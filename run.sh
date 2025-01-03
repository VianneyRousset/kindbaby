#!/usr/bin/env sh

DOCKER_COMPOSE_FILE="compose.yaml"
ENVIRONMENT_FILE=".env"

docker compose \
  --file "${DOCKER_COMPOSE_FILE}" \
  --env-file "${ENVIRONMENT_FILE}" \
  up
