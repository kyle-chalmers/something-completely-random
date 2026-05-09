#!/usr/bin/env python3
"""
Aggregate all dreams/{id}/dream.json files into meta/manifest.json.

Each dream's metadata is read, validated lightly, and combined with a generated
gallery-level summary (assembly time, count, average scores).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DREAMS_DIR = REPO_ROOT / "dreams"
META_DIR = REPO_ROOT / "meta"
MANIFEST_PATH = META_DIR / "manifest.json"


def load_dream(dream_dir: Path) -> dict | None:
    dream_json = dream_dir / "dream.json"
    if not dream_json.exists():
        print(f"  ⚠️  {dream_dir.name}: dream.json missing — skipping", file=sys.stderr)
        return None
    try:
        with dream_json.open() as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  {dream_dir.name}: invalid JSON — {e}", file=sys.stderr)
        return None


def main() -> int:
    if not DREAMS_DIR.exists():
        print(f"No dreams directory at {DREAMS_DIR}", file=sys.stderr)
        return 1

    dream_dirs = sorted(d for d in DREAMS_DIR.iterdir() if d.is_dir())
    dreams: list[dict] = []
    for d in dream_dirs:
        dream = load_dream(d)
        if dream:
            dreams.append(dream)
            print(f"  ✓ {d.name}: {dream.get('title', '(untitled)')}")

    novelty = [int(d.get("novelty_score", 0)) for d in dreams if d.get("novelty_score")]
    buildability = [int(d.get("buildability_score", 0)) for d in dreams if d.get("buildability_score")]

    manifest = {
        "name": "Reverie",
        "subtitle": "A Dream Gallery",
        "assembled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dreams_count": len(dreams),
        "average_novelty": round(sum(novelty) / len(novelty), 2) if novelty else None,
        "average_buildability": round(sum(buildability) / len(buildability), 2) if buildability else None,
        "dreams": dreams,
    }

    META_DIR.mkdir(exist_ok=True)
    with MANIFEST_PATH.open("w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print()
    print(f"✓ Wrote {MANIFEST_PATH}")
    print(f"  · {manifest['dreams_count']} dreams")
    if manifest["average_novelty"]:
        print(f"  · avg novelty: {manifest['average_novelty']}")
    if manifest["average_buildability"]:
        print(f"  · avg buildability: {manifest['average_buildability']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
