#!/usr/bin/env bash


echo "Waiting for postgres..."

while ! nc -z $AUTH_POSTGRES_HOST $AUTH_POSTGRES_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

echo "Waiting for Redis..."

while ! nc -z $AUTH_REDIS_HOST $AUTH_REDIS_PORT; do
    sleep 0.1
done


echo "Redis started"
gunicorn wsgi_run:run --workers 4 -k gevent --bind 0.0.0.0:8000