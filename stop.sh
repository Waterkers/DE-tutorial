#!/usr/bin/env bash
# Stop the DE practical. Your notebooks stay in the practical/ folder.
cd "$(dirname "$0")"
docker compose down
