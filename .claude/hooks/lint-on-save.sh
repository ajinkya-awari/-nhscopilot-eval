#!/usr/bin/env bash
set -u

if command -v python >/dev/null 2>&1; then
  python - <<'PY'
import json
from pathlib import Path
settings = Path('.claude/settings.json')
if settings.exists():
    json.loads(settings.read_text(encoding='utf-8'))
PY
else
  echo "Python is required to validate settings.json."
  exit 2
fi

if rg -n -i 'sk-[A-Za-z0-9]{20,}|gsk_[A-Za-z0-9]{20,}|wandb_[A-Za-z0-9]{20,}' . --glob '!*.pyc' --glob '!.git/**' >/dev/null 2>&1; then
  echo "Possible secret detected; inspect without printing it."
  exit 2
fi
exit 0
