#!/bin/bash
# Regenerate the whole PPS package from the vector sources. Needs: brew install librsvg potrace; a venv with _build/requirements.txt; node (for the previz syntax check).
set -e; cd "$(dirname "$0")"
PY="${PY:-$(ls -d ../../../.venv/bin/python ../.venv/bin/python .venv/bin/python 2>/dev/null | head -1)}"; PY="${PY:-python3}"
"$PY" geometry.py && "$PY" export.py && "$PY" ae.py && "$PY" gen_previz.py && "$PY" gen_sheet.py && "$PY" contact.py
echo "regenerated — look at _build/contact.jpg"
