#!/usr/bin/env bash
# Run every solution notebook in the container, so teacher/solutions/ contains the
# expected outputs. Fails if any cell gives an error.
# Output that arrives in pieces (timing differs between computers) is merged
# afterwards (--coalesce-streams), so reruns on any computer give identical files.
#   tools/run_solutions.sh            uses the image from docker-compose.yml / .env
#   tools/run_solutions.sh IMAGE      uses the given image (as in CI)
set -euo pipefail
cd "$(dirname "$0")/.."
image="${1:-$(docker compose config --images)}"
docker run --rm -u root -e NB_UID="$(id -u)" -e NB_GID="$(id -g)" \
    -v "$PWD/teacher:/home/jovyan/teacher" "$image" \
    bash -c 'cd teacher/solutions && status=0
             for f in en/*.ipynb de/*.ipynb; do
               # Merging is a second pass: within one call it runs before execution.
               if jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 --ExecutePreprocessor.record_timing=False "$f" >/dev/null 2>&1 &&
                  jupyter nbconvert --to notebook --inplace --coalesce-streams "$f" >/dev/null 2>&1
               then echo "ok   $f"; else echo "FAIL $f"; status=1; fi
             done
             exit $status' 2>&1 | grep -E '^(ok|FAIL)'
