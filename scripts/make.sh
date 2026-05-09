#!/usr/bin/env bash
# Reverie · build pipeline
# Re-aggregates the manifest and runs all verification.

set -euo pipefail

cd "$(dirname "$0")/.."

echo "── building manifest ──"
python3 scripts/build_manifest.py

echo
echo "── verifying dream structure ──"
python3 scripts/verify_dreams.py

echo
echo "── checking dream JS ──"
python3 scripts/check_dream_js.py

echo
echo "✓ Reverie ready. Open index.html or run: python3 -m http.server 8000"
