#!/usr/bin/env bash


echo "Waiting for Kafka..."
while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
    sleep 0.1
done

echo "Kafka started"

echo "Waiting for ZooKeeper..."

while ! nc -z $ZOOKEEPER_HOST $ZOOKEEPER_PORT; do
    sleep 0.1
done


echo "ZooKeeper started"

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000