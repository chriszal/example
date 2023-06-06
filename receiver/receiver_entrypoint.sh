#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until nc -z -v -w30 "$host" 5672; do
  echo "RabbitMQ is unavailable - sleeping"
  sleep 5
done

echo "RabbitMQ is up - executing command"
exec $cmd
