#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
BACK="$ROOT/liri-back"
if [ -d "$ROOT/LiriPag" ]; then PAG="$ROOT/LiriPag"; else PAG="$ROOT/../LiriPag"; fi
PY="${PYTHON:-python3}"

for p in 9081 8080; do
  if ss -ltn "sport = :$p" | grep -q LISTEN; then
    echo "Puerto $p ocupado, no arranco." >&2; exit 1
  fi
done

pids=()
cleanup() { trap - INT TERM EXIT; kill "${pids[@]}" 2>/dev/null; wait; }
trap cleanup INT TERM EXIT

(cd "$BACK" && exec "$PY" main.py) & pids+=($!)
(cd "$PAG"  && exec "$PY" app.py)  & pids+=($!)

echo "liri-back :9081 | LiriPag :8080 | Ctrl+C para cerrar"
wait -n
echo "Un proceso terminó; cerrando el otro." >&2
