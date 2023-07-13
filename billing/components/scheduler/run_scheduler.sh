#!/usr/bin/env bash

echo "Waiting for PSQL..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "PSQL started"

cd src
python main.py