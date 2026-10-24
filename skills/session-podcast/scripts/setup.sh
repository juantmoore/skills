#!/usr/bin/env bash
# One-time setup for Kokoro TTS. Creates a Python 3.10–3.12 venv (Kokoro does not support 3.13+).
# usage: setup.sh [venv_dir]   (default: $KOKORO_VENV or ~/.venvs/kokoro)
set -euo pipefail
VENV="${1:-${KOKORO_VENV:-$HOME/.venvs/kokoro}}"

command -v ffmpeg >/dev/null || brew install ffmpeg
command -v espeak-ng >/dev/null || brew install espeak-ng   # pronunciation fallback for unknown words

PY=""
for c in python3.12 python3.11 python3.10 "$HOME/.local/bin/python3.11"; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [[ -z "$PY" ]]; then
  echo "Need Python 3.10–3.12 (e.g. 'uv python install 3.11' or 'brew install python@3.12')." >&2; exit 1
fi

"$PY" -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q "kokoro>=0.9.4" soundfile
# First run downloads the Kokoro-82M weights (~330 MB) and a spaCy English model.
"$VENV/bin/python" -c "from kokoro import KPipeline; KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M'); print('kokoro ready')"
echo "Kokoro venv: $VENV  (use: $VENV/bin/python scripts/render.py ...)"
