#!/bin/bash

set -o errexit

set -o pipefail

set  -o nounset

python << END
import sys, time, psycopg2

suggest_unrecoverable_after = 30
start = time.time()
while True:
  try:
    psycopg2.connect(
    dbname="${POSTGRES_DB}",
    user="${POSTGRES_USER}",
    port="${POSTGRES_PORT}",
    password="${POSTGRES_PASSWORD}",
    host="${POSTGRES_HOST}"
    )
    sys.stderr.write(f" PostgresSQL is Available ... \n")

  except  Exception as E:
    sys.stderr.write("Waiting for PostgresSQL to became available \n")
    if time.time() - start > suggest_unrecoverable_after :
      sys.stderr.write(f"got Error to connect : {E} \n")
      time.sleep(3)

END

exec "$@"