#!/usr/bin/env bash


echo "Waiting for postgres..."

while ! nc -z $NOTF_POSTGRES_HOST $NOTF_POSTGRES_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

gunicorn --bind 0.0.0.0:8000 adminpanel.wsgi