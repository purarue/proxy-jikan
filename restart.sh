#!/bin/bash

THIS_DIR="$(dirname ${BASH_SOURCE[0]})"
cd "$THIS_DIR"

export PROXY_PORT="${PROXY_PORT:?'no proxy port set'}"
export PROXY_TOKEN="${PROXY_TOKEN:?'no proxy token set'}"

DJ="../docker-jikan"

[ ! -d "$DJ" ] && {
  printf "Expected docker-jikan at %s" "$DJ"
  exit 1
}

forever stopall

forever start ---uid "docker" --logFile "${HOME}/docker.log" \
 --append --spinSleepTime 10000 --minUptime 10000 --sourceDir "$DJ" -c "sh" "run.sh"


forever start ---uid "proxy" --logFile "${HOME}/proxy.log" \
 --append --spinSleepTime 10000 --minUptime 10000 --sourceDir "$THIS_DIR" -c "pipenv run python" "app.py"
