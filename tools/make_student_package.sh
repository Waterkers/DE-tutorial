#!/usr/bin/env bash
# Build the files to hand out to students, in dist/:
#   de-practical-students.zip   start/stop scripts, compose file, student notebooks
#   de-practical-image.tar.gz   the Docker image, for computers without fast internet
#                                (only with --with-image; about 1 GB)
# The teacher/ and tools/ folders are left out.
set -euo pipefail
cd "$(dirname "$0")/.."
image="$(docker compose config --images)"
mkdir -p dist
rm -f dist/de-practical-students.zip
files=(practical docker docker-compose.yml LICENSE LICENSE-CC-BY-4.0.txt THIRD_PARTY_NOTICES.md
       start.sh start.command start_de.command start.bat start_de.bat stop.sh stop.bat)
# A local .env (e.g. DE_IMAGE for a registry image) goes to the students too.
if [ -f .env ]; then
    files+=(.env)
fi
zip -qr dist/de-practical-students.zip "${files[@]}" -x '*.ipynb_checkpoints*' '*/__pycache__/*'
echo "wrote dist/de-practical-students.zip"
if [ "${1:-}" = "--with-image" ]; then
    docker save "$image" | gzip > dist/de-practical-image.tar.gz
    echo "wrote dist/de-practical-image.tar.gz ($image)"
fi
