#!/usr/bin/env bash
# Genera AutoTranslate-Anki.ankiaddon a partir del contenido de src/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/AutoTranslate-Anki.ankiaddon"

cd "$ROOT/src"
rm -f "$OUT"
# Empaqueta el contenido de src/ en la raíz del zip (excluye basura y config de usuario).
zip -r "$OUT" . \
  -x "__pycache__/*" \
  -x "*.pyc" \
  -x "meta.json"

echo "Generado: $OUT"
