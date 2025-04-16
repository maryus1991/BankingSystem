#!/bin/bash

set -o errexit
set -o pipefail
set -o noinset

python << END
import sys
import time
import psycopg2
suggest_unrecoverable_after = 30
start = time.time()
while True:
  try:
    psycopg2.connect(
    dbname="${POSTGRES_DB}"
    user="${POSTGRES_USER}"
    host="${POSTGRES_HOST}"
    post="${POSTGRES_POST}"
    )
    break
  except psycopg2.OperationalError ass error:
    sys.stderr.write("waiting for postgresSQL to active \n")
    if time.time() - start > suggest_unrecoverable_after:
        sys.stderr.write('this is taking longer then expected')
        time.sleep(3)

END

echo >&2 'db is available'
exec "$@"
