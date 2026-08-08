#!/usr/bin/env python3
"""Check markdown relative links under skills/ and docs/guide/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "#",
)


def iter_markdown() -> list[Path]:
    paths = list((ROOT / "skills").rglob("*.md"))
    guide = ROOT / "docs" / "guide"
    if guide.is_dir():
        paths.extend(guide.rglob("*.md"))
    return sorted(path for path in paths if path.is_file())


def check_file(path: Path) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith(SKIP_PREFIXES):
            continue
        if " " in target and not target.startswith("<"):
            # Ignore titles in links like (path "title")
            target = target.split(" ", 1)[0]
        target = target.split("#", 1)[0]
        if not target:
            continue
        # Template placeholders in skill prompts, e.g. [PR #123](url) or ({PATH})
        if target in {"url", "path", "href"} or "{" in target or "<" in target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            findings.append(f"{path.relative_to(ROOT)}: escapes repo via {target}")
            continue
        if not resolved.exists():
            findings.append(
                f"{path.relative_to(ROOT)}: broken relative link -> {target}"
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    findings: list[str] = []
    for path in iter_markdown():
        findings.extend(check_file(path))
    for finding in findings:
        print(f"ERROR: {finding}")
    print(f"markdown link check: {len(findings)} error(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
