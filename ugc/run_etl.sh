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

echo "Waiting for Clickhouse..."

while ! nc -z $CLICKHOUSE_HOST $CLICKHOUSE_PORT; do
    sleep 0.1
done

echo "Clickhouse started"

python etl_run.py