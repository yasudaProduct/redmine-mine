#!/bin/bash

echo "Waiting for Redmine to be ready..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -s http://redmine:3000 > /dev/null; then
        echo "Redmine is ready!"
        exit 0
    fi
    echo "Attempt $attempt of $max_attempts: Redmine is not ready yet - waiting..."
    sleep 10
    attempt=$((attempt + 1))
done

echo "Redmine failed to become ready after $max_attempts attempts"
exit 1 