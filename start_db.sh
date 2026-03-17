#!/usr/bin/env bash
set -euo pipefail

# Load only Postgres vars from .env
# - grep: grab only lines starting with POSTGRES_ or DB_CONTAINER_NAME
# - sed 's/ *= */=/': strip spaces around the = sign
# - sed 's/"//g': strip any surrounding quotes
if [ -f .env ]; then
  export $(grep -E '^(POSTGRES_|DB_CONTAINER_NAME)' .env | sed 's/ *= */=/' | sed 's/"//g' | xargs)
else
  echo "Error: .env file not found"
  exit 1
fi

# If container already exists (stopped or running), just start it
if docker ps -a --format '{{.Names}}' | grep -q "^${DB_CONTAINER_NAME}$"; then
  echo "Container '${DB_CONTAINER_NAME}' already exists — starting it..."
  docker start "${DB_CONTAINER_NAME}"
else
  echo "Creating and starting container '${DB_CONTAINER_NAME}'..."
  docker run --name "${DB_CONTAINER_NAME}" \
    -e POSTGRES_USER="${POSTGRES_USER}" \
    -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -e POSTGRES_DB="${POSTGRES_DB}" \
    -p "${POSTGRES_PORT}:5432" \
    -d postgres:15
fi

echo "Done. Postgres is running on port ${POSTGRES_PORT}."
echo "Connection string: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}"
