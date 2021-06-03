#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"