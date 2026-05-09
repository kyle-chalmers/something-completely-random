#!/usr/bin/env python3
"""Inject a single <script src=...dream-nav.js> tag into each dream's index.html.

Idempotent: skips files that already include the script tag.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DREAMS = REPO / "dreams"
TAG = '<script src="../../assets/dream-nav.js" defer></script>'


def inject(html_path: Path) -> str:
    text = html_path.read_text(encoding="utf-8")
    if "dream-nav.js" in text:
        return "skipped (already present)"
    if "</body>" not in text:
        return "ERROR: no </body> tag"
    new = text.replace("</body>", f"  {TAG}\n</body>")
    html_path.write_text(new, encoding="utf-8")
    return "injected"


def main() -> int:
    rc = 0
    for d in sorted(DREAMS.iterdir()):
        if not d.is_dir():
            continue
        html = d / "index.html"
        if not html.exists():
            print(f"  ⚠️  {d.name}: index.html missing")
            rc = 1
            continue
        result = inject(html)
        symbol = "✓" if "ERROR" not in result else "✗"
        print(f"  {symbol} {d.name}: {result}")
        if "ERROR" in result:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
