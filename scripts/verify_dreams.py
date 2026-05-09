#!/usr/bin/env python3
"""Lightweight structural verification of each dream's HTML and JSON."""
from __future__ import annotations

import html.parser
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DREAMS_DIR = REPO_ROOT / "dreams"


class TagBalancer(html.parser.HTMLParser):
    """Tracks tag open/close balance, ignoring void tags."""
    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return  # `<meta />` triggers a synthetic endtag in html.parser; ignore.
        if not self.stack:
            self.errors.append(f"unexpected closing </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        else:
            # try to recover by popping until we find the matching tag
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.stack.pop()
                if self.stack:
                    self.stack.pop()
            else:
                self.errors.append(
                    f"closing </{tag}> doesn't match opened <{self.stack[-1] if self.stack else '?'}>"
                )

    def handle_startendtag(self, tag, attrs):
        # Self-closing tag like <meta />. In HTML5, treat as start-only for void tags.
        if tag not in self.VOID:
            self.stack.append(tag)

    def remaining(self):
        return self.stack


def check_dream(dream_dir: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []
    name = dream_dir.name

    html_path = dream_dir / "index.html"
    json_path = dream_dir / "dream.json"
    notes_path = dream_dir / "notes.md"

    if not html_path.exists():
        issues.append("index.html missing")
    if not json_path.exists():
        issues.append("dream.json missing")
    if not notes_path.exists():
        issues.append("notes.md missing")

    if html_path.exists():
        text = html_path.read_text(encoding="utf-8")
        # Required structural pieces
        for needle, label in [
            ("<!DOCTYPE html>", "DOCTYPE"),
            ('class="return-ribbon"', "return ribbon"),
            ('class="wake-log-toggle"', "wake-log toggle"),
            ('class="wake-log"', "wake-log panel"),
            ("../../style.css", "shared CSS link"),
            ("</html>", "</html> closer"),
        ]:
            if needle not in text:
                issues.append(f"missing {label}")
        # Tag balance
        balancer = TagBalancer()
        try:
            balancer.feed(text)
            balancer.close()
            if balancer.errors:
                issues.append(f"html tag mismatch: {balancer.errors[0]}")
            if balancer.remaining():
                issues.append(f"unclosed tags: {balancer.remaining()[:3]}")
        except Exception as e:
            issues.append(f"html parse error: {e}")
        # Forbidden patterns
        forbid = [
            (r"<script[^>]*src=\s*\"https?://(?!fonts\.|cdnjs\.cloudflare\.com/(?:ajax/libs/(?:fontawesome)))", "external script CDN"),
        ]
        # Count unclosed style/script blocks
        for tag in ["script", "style"]:
            opens = len(re.findall(f"<{tag}[^/]*>", text))
            closes = len(re.findall(f"</{tag}>", text))
            if opens != closes:
                issues.append(f"<{tag}> open/close mismatch: {opens} open vs {closes} close")

    if json_path.exists():
        try:
            d = json.loads(json_path.read_text(encoding="utf-8"))
            for key in ["id", "persona", "title", "essence", "description", "wake_log"]:
                if key not in d:
                    issues.append(f"dream.json missing key '{key}'")
        except json.JSONDecodeError as e:
            issues.append(f"dream.json invalid: {e}")

    return (len(issues) == 0, issues)


def main() -> int:
    if not DREAMS_DIR.exists():
        print("no dreams directory", file=sys.stderr)
        return 1
    all_ok = True
    for d in sorted(DREAMS_DIR.iterdir()):
        if not d.is_dir():
            continue
        ok, issues = check_dream(d)
        symbol = "✓" if ok else "✗"
        print(f"  {symbol} {d.name}")
        for issue in issues:
            print(f"      · {issue}")
        if not ok:
            all_ok = False
    print()
    print("all dreams verified ✓" if all_ok else "some dreams need attention ✗")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
