#!/bin/bash

set -o errexit
set -o nounset

readonly cmd="$*"

# Print build information
echo "------------------------------------------------------------------------------"
echo " - Release: ${NOVA_RELEASE:-No CI build}"
echo " - Build: ${NOVA_BUILD_ID:-No CI build}"
echo " - Build pipeline: ${NOVA_PIPELINE_URL:-No CI build}"
echo "------------------------------------------------------------------------------"

postgres_ready () {
  # Check that postgres is up and running on port `5432`:
  dockerize -wait 'tcp://db:5432' -timeout 5s
}

if [ "$1" == "nginx" ]; then
  echo "Starting nginx"
else
  # We need this line to make sure that this container is started
  # after the one with postgres:
  until postgres_ready; do
    >&2 echo 'Postgres is unavailable - sleeping'
  done

  # It is also possible to wait for other services as well: redis, elastic, mongo
  >&2 echo 'Postgres is up - continuing...'
fi

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
