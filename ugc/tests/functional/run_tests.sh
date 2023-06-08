#!/usr/bin/env bash

echo "Waiting for First Mongos..."
while ! nc -z $MONGOS1_HOST $MONGOS1_PORT; do
    sleep 0.1
done

echo "First Mongos started"

echo "Waiting for second Mongos..."

while ! nc -z $MONGOS2_HOST $MONGOS2_PORT; do
    sleep 0.1
done

python -m pytest .