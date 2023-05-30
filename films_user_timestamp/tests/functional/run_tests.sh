#!/usr/bin/env bash

echo "Waiting for Kafka..."
while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
    sleep 0.2
done

echo "Kafka started"

echo "Waiting for UGC..."

while ! curl "$UGC_URL"; do
    sleep 0.2
done

echo "UGC Started"

echo "Waiting for ZooKeeper..."

echo "Waiting for Clickhouse..."

while ! nc -z $CLICKHOUSE_HOST $CLICKHOUSE_PORT; do
    sleep 0.1
done

echo "Clickhouse started"

python -m pytest .