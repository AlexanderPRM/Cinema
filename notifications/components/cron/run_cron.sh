#!/usr/bin/env bash

echo "Waiting for RabbitMQ..."

while ! nc -z $NOTF_RABBITMQ_HOST $NOTF_RABBITMQ_PORT; do
    sleep 0.1
done

echo "RabbitMQ started"

echo "Waiting for API..."

while ! nc -z $NOTF_API_HOST $NOTF_API_PORT; do
    sleep 0.1
done

echo "API started"

python main.py