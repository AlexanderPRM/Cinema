#!/usr/bin/env bash


echo "Waiting for elastic..."

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
    sleep 0.1
done

echo "ElasticSearch started"

python main.py