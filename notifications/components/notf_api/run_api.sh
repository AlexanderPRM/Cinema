#!/usr/bin/env bash


echo "Waiting for RabbitMQ..."

while ! nc -z $NOTF_RABBITMQ_HOST $NOTF_RABBITMQ_PORT; do
    sleep 0.1
done

echo "RabbitMQ started"

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001