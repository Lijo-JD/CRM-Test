#!/usr/bin/env bash
set -eu

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python3 --version >/dev/null 2>&1 || { echo "Python 3 is required but not installed."; exit 1; }
node --version >/dev/null 2>&1 || { echo "Node.js is required but not installed."; exit 1; }

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt

cd frontend
npm install
cd "$ROOT_DIR"

echo "Generation complete. Run ./run.sh to start the app."
