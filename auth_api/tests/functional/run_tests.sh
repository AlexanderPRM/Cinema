#!/usr/bin/env bash

echo "Waiting for postgres..."

while ! nc -z $AUTH_POSTGRES_HOST $AUTH_POSTGRES_PORT; do
    sleep 0.1
done

sleep 0.1
echo "Postgres started"

echo "Waiting for Redis..."

while ! nc -z $AUTH_REDIS_HOST $AUTH_REDIS_PORT; do
    sleep 0.1
done

sleep 0.1
echo "Redis started"

python -m pytest .