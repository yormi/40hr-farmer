#!/usr/bin/env bash
# Local hot-reload dev server for the 40hr Farmer landing page.
#
# Serves landing/ as the document root on http://localhost:8888, with
# /assets and /drew-season mounted from their sibling directories so
# absolute paths in landing/index.html resolve the same way they do
# on the deployed GitHub Pages site.
#
# Usage:
#   ./scripts/dev-server.sh
#
# Stop:
#   pkill -f live-server
#
# Requires: fnm with Node 22 available, npx (ships with Node).

set -euo pipefail

PORT=8888
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

# Node 22 is required. live-server's dependency graph doesn't resolve on Node 16.
eval "$(fnm env)"
fnm use 22 >/dev/null

# Free the port if a previous server is still bound.
if ss -tln 2>/dev/null | grep -q ":${PORT} "; then
  echo "Port ${PORT} in use, killing previous server..."
  pkill -f "http\.server ${PORT}" 2>/dev/null || true
  pkill -f "live-server.*${PORT}" 2>/dev/null || true
  sleep 1
fi

cd "${REPO_ROOT}"

echo "Starting live-server on http://localhost:${PORT} (root: landing/) ..."
exec npx --yes live-server landing \
  --port="${PORT}" \
  --no-browser \
  --quiet \
  --mount=/assets:./assets \
  --mount=/drew-season:./drew-season
