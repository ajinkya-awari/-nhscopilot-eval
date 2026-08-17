#!/usr/bin/env bash
set -u

# Local evidence gate only. It never uploads, publishes, deletes, or reads secret values.
changed="$(git diff --cached --name-only -- '*.py' '*.md' '*.json' '*.yml' '*.yaml' 2>/dev/null || true)"
if [ -z "$changed" ]; then
  echo "No supported staged files; Project 09 checks skipped."
  exit 0
fi

if command -v python >/dev/null 2>&1; then
  python -m compileall -q src scripts tests 2>/dev/null || exit 2
  python -m pytest -q 2>/dev/null || exit 2
else
  echo "Python is required for Project 09 checks."
  exit 2
fi

echo "NHSCopilot-Eval local checks passed."
exit 0
