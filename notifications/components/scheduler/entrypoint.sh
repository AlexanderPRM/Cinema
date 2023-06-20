#!/usr/bin/env bash

echo "Waiting for postgres..."

while ! nc -z $NOTF_POSTGRES_HOST $NOTF_POSTGRES_PORT; do
    sleep 0.1
done

echo "Postgres started"

echo "Waiting for RabbitMQ..."

while ! nc -z $NOTF_RABBITMQ_HOST $NOTF_RABBITMQ_PORT; do
    sleep 0.1
done

echo "RabbitMQ started"

python main.py