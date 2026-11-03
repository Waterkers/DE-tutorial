#!/usr/bin/env bash
# Start the DE practical and open it in the browser.
#   ./start.sh       English
#   ./start.sh de    Deutsch
# NO_BROWSER=1 ./start.sh   starts without opening the browser.
set -euo pipefail
cd "$(dirname "$0")"

lang="${1:-en}"
case "$lang" in
  en) msg_start="Starting the practical (the first start can take a minute)..."
      msg_fail="Docker is not running. Start Docker Desktop and try again."
      msg_ready="Ready: http://localhost:8889  -  to stop, run ./stop.sh"
      msg_wait="JupyterLab did not start. Show the error with: docker compose logs" ;;
  de) msg_start="Das Praktikum wird gestartet (der erste Start kann eine Minute dauern)..."
      msg_fail="Docker läuft nicht. Starte Docker Desktop und versuche es noch einmal."
      msg_ready="Fertig: http://localhost:8889  -  zum Beenden: ./stop.sh"
      msg_wait="JupyterLab ist nicht gestartet. Fehler anzeigen mit: docker compose logs" ;;
  *)  echo "Usage: $0 [en|de]"; exit 1 ;;
esac

docker info >/dev/null 2>&1 || { echo "$msg_fail"; exit 1; }
echo "$msg_start"

export PRACTICAL_LANG="$lang" HOST_UID="$(id -u)" HOST_GID="$(id -g)"
docker compose up -d --no-build

url="http://localhost:8889/lab/tree/practical/$lang"
for _ in $(seq 1 60); do
  if curl -fs -o /dev/null http://localhost:8889/api; then
    echo "$msg_ready"
    if [ -n "${NO_BROWSER:-}" ]; then :
    elif [ "$(uname)" = "Darwin" ]; then open "$url"
    elif command -v xdg-open >/dev/null; then xdg-open "$url" >/dev/null 2>&1 &
    fi
    exit 0
  fi
  sleep 1
done
echo "$msg_wait"
exit 1
