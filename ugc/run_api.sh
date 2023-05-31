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


echo "Second Mongos started"

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000