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
python main.py