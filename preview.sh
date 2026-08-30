#!/usr/bin/env bash
# One-command live site preview: builds the web version of the app and serves
# it — UI + API on the same port — at http://localhost:5555
#
#   ./preview.sh            # build (first run) + serve on 5555
#   PORT=8080 ./preview.sh  # different port
#   REBUILD=1 ./preview.sh  # force a fresh web build
set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-5555}"

if [ ! -d backend/node_modules ]; then
  echo "==> Installing backend dependencies..."
  (cd backend && npm install)
fi
if [ ! -d mobile/node_modules ]; then
  echo "==> Installing mobile dependencies..."
  (cd mobile && npm install)
fi

if [ ! -f mobile/dist/index.html ] || [ "${REBUILD:-0}" = "1" ]; then
  echo "==> Building the web app (expo export)..."
  (cd mobile && npx expo export --platform web)
fi

echo "==> Starting the site on http://localhost:${PORT}  (Ctrl+C to stop)"
cd backend
PORT="$PORT" STATIC_DIR="../mobile/dist" exec npm run dev
