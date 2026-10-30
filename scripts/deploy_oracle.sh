#!/usr/bin/env bash
# Apply an already-reviewed main branch update on the EXISTING Oracle Cloud VPS.
# This script does not store keys or modify the Nginx configuration.
set -Eeuo pipefail

SERVICE="${JESUS_REELS_SERVICE:-jesus-reels}"
PORT="${JESUS_REELS_PORT:-8050}"
REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if ! command -v git >/dev/null 2>&1 || ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: git and curl must be installed." >&2
    exit 1
fi
if [[ ! -d .git ]]; then
    echo "ERROR: Run from your existing GitHub-cloned FB repository." >&2
    exit 1
fi
if [[ "$(git branch --show-current)" != "main" ]]; then
    echo "ERROR: Switch to main before deployment: git switch main" >&2
    exit 1
fi
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERROR: Tracked local changes detected. Commit or back them up first." >&2
    exit 1
fi

PREVIOUS="$(git rev-parse --short=12 HEAD)"
echo "Current checkout: $PREVIOUS"
git fetch --prune origin main
git merge --ff-only origin/main
TARGET="$(git rev-parse --short=12 HEAD)"
echo "Deploying verified checkout: $TARGET"

# Reuse the service's local Python environment when present; do not attempt
# a system-wide pip install on Ubuntu, which could alter unrelated services.
if [[ -x .venv/bin/python ]]; then
    .venv/bin/python -m pip install -r requirements.txt
elif [[ -x venv/bin/python ]]; then
    venv/bin/python -m pip install -r requirements.txt
else
    echo "INFO: No local venv found; existing environment is unchanged."
    echo "If a dependency is missing, install it into your systemd service's environment."
fi

sudo systemctl restart "$SERVICE"
sudo systemctl is-active --quiet "$SERVICE" || {
    sudo systemctl status "$SERVICE" --no-pager
    echo "ERROR: Service did not start. Previous checkout was $PREVIOUS" >&2
    exit 1
}

echo "Checking local HTTP application health..."
HEALTH="$(curl --fail --silent --show-error --retry 5 --retry-delay 2 --max-time 10 "http://127.0.0.1:$PORT/health")"
echo "$HEALTH"
VERSION="$(curl --fail --silent --show-error --retry 3 --retry-delay 2 --max-time 10 "http://127.0.0.1:$PORT/api/version")"
echo "$VERSION"
if [[ "$VERSION" != *"$TARGET"* ]]; then
    echo "WARNING: HTTP server did not report the expected commit $TARGET." >&2
    echo "Check systemd WorkingDirectory and ExecStart:" >&2
    echo "  sudo systemctl cat $SERVICE" >&2
    exit 1
fi
echo "SUCCESS: Running checkout matches GitHub main ($TARGET)."
echo "Open: https://132-145-202-1.sslip.io"
echo "Verify: https://132-145-202-1.sslip.io/api/version"
