#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python << END
import sys
import time
import psycopg2
suggest_unrecoverable_after = 30
start = time.time()
while True:
  try:
    psycopg2.connect(
    dbname="${POSTGRES_DB}",
    user="${POSTGRES_USER}",
    host="${POSTGRES_HOST}",
    port="${POSTGRES_PORT}",
    password="${POSTGRES_PASSWORD}"
    )
    break
  except psycopg2.OperationalError as error:
    sys.stderr.write("waiting for postgresSQL to active \n")
    print(error)
    if time.time() - start > suggest_unrecoverable_after:
        sys.stderr.write('this is taking longer then expected')
    time.sleep(3)

END

echo >&2 'db is available'
exec "$@"
