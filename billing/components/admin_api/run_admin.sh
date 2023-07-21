#!/usr/bin/env bash

echo "Waiting for PSQL..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "PSQL started"

echo "Waiting for RabbitMQ..."

while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
    sleep 0.1
done

echo "RABBITMQ started"

cd src
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000