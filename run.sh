#!/usr/bin/env bash
set -eu

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "Environment not generated yet. Run ./generate.sh first."
  exit 1
fi

. .venv/bin/activate
export PORT=8001
(
  cd backend
  python -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
) &

cd frontend
npm run dev
