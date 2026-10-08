#!/usr/bin/env bash
# Run a skill script inside a private venv that has python-docx.
# Usage: scripts/run.sh docx_links.py extract draft.docx
# The venv is created once at ~/.cache/internal-linking/venv.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
venv="${INTERNAL_LINKING_VENV:-$HOME/.cache/internal-linking/venv}"
if [ ! -x "$venv/bin/python" ] || ! "$venv/bin/python" -c "import docx" 2>/dev/null; then
  echo "setting up $venv (one time)..." >&2
  python3 -m venv "$venv"
  "$venv/bin/python" -m pip install --quiet --disable-pip-version-check python-docx
fi
script="$1"; shift
exec "$venv/bin/python" "$here/$script" "$@"
