#!/usr/bin/env python3
"""Extract <script> blocks from each dream's index.html and check syntax with node."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DREAMS_DIR = REPO_ROOT / "dreams"

SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.DOTALL | re.IGNORECASE)
SRC_RE = re.compile(r'src\s*=\s*["\']([^"\']+)["\']')


def check_dream(dream_dir: Path) -> tuple[int, list[str]]:
    html = (dream_dir / "index.html").read_text(encoding="utf-8")
    issues: list[str] = []
    block_idx = 0
    blocks_checked = 0
    for match in SCRIPT_RE.finditer(html):
        block_idx += 1
        attrs = match.group(1) or ""
        body = match.group(2) or ""
        # Skip external scripts (we don't have any but defensively check).
        if SRC_RE.search(attrs):
            continue
        if not body.strip():
            continue
        with tempfile.NamedTemporaryFile(
            "w", suffix=".js", delete=False, encoding="utf-8"
        ) as tmp:
            # Wrap in IIFE so re-declarations across blocks don't collide,
            # and so that 'await' at top-level doesn't error in strict module mode.
            tmp.write("(async () => {\n" + body + "\n})();\n")
            tmp_path = tmp.name
        try:
            res = subprocess.run(
                ["node", "--check", tmp_path],
                capture_output=True, text=True, timeout=5,
            )
            if res.returncode != 0:
                issues.append(f"block {block_idx}: {res.stderr.strip().splitlines()[0]}")
            else:
                blocks_checked += 1
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    return blocks_checked, issues


def main() -> int:
    all_ok = True
    for d in sorted(DREAMS_DIR.iterdir()):
        if not d.is_dir():
            continue
        n, issues = check_dream(d)
        symbol = "✓" if not issues else "✗"
        print(f"  {symbol} {d.name}: {n} script blocks ok")
        for issue in issues:
            print(f"      · {issue}")
        if issues:
            all_ok = False
    print()
    print("all dream JS valid ✓" if all_ok else "some dreams have JS issues ✗")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
