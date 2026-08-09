#!/usr/bin/env python3
"""Check ystack's public naming boundary and legacy compatibility entries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

REQUIRED_SNIPPETS = {
    "README.md": ("# ystack", "Go7hic/ystack", "`/ystack`"),
    "INSTALL.md": ("Go7hic/ystack", "/setup-ystack", "ystack-models"),
    "skills/ystack/SKILL.md": ("name: ystack", "# ystack", "../pstack/references"),
    "skills/setup-ystack/SKILL.md": ("name: setup-ystack", "# Setup ystack"),
    "skills/pstack/SKILL.md": ("Legacy compatibility alias", "../ystack/SKILL.md"),
    "skills/setup-pstack/SKILL.md": ("Legacy compatibility alias", "../setup-ystack/SKILL.md"),
}

# Construct the retired repository slug without embedding it literally in this
# file; the checker scans repository text, including maintenance scripts.
OLD_REPO = "Go7hic" + "/" + "pstack"
STALE_REPO_SLUGS = (OLD_REPO, "github.com/" + OLD_REPO)
TEXT_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".toml", ".txt"}


def text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if path.resolve() == SELF:
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    errors: list[str] = []

    for rel, snippets in REQUIRED_SNIPPETS.items():
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing required branding file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{rel}: missing required snippet {snippet!r}")

    for path in text_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for slug in STALE_REPO_SLUGS:
            if slug in text:
                errors.append(f"{rel}: stale repository slug {slug!r}")

    manifest_path = ROOT / "UPSTREAM_MANIFEST.json"
    if manifest_path.is_file():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        portable = data.get("portable", {})
        if portable.get("public_name") != "ystack":
            errors.append("UPSTREAM_MANIFEST.json: portable.public_name must be 'ystack'")
        if "pstack" not in portable.get("legacy_names", []):
            errors.append("UPSTREAM_MANIFEST.json: legacy_names must include 'pstack'")

    for error in errors:
        print(f"ERROR: {error}")
    print(f"branding check: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
