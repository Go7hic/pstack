#!/usr/bin/env python3
"""Validate a pstack model override document against the portable schema."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "skills" / "pstack" / "references" / "model-override.schema.json"
KNOWN_ROLES = {"fast_explore", "feature_impl", "bug_impl", "judgment", "critic"}
ALIAS = {"inherit-parent", "auto"}


def load_override(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".json"}:
        return json.loads(text)
    # Markdown override files: extract fenced JSON or simple `role: value` lines.
    fence = re.search(r"```json\n(.*?)\n```", text, re.S)
    if fence:
        return json.loads(fence.group(1))
    roles: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"`?([a-z_]+)`?\s*:\s*`?([^`]+)`?\s*$", line.strip())
        if match and match.group(1) in KNOWN_ROLES:
            roles[match.group(1)] = match.group(2).strip()
    return {"schema_version": 1, "roles": roles}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if data.get("schema_version") != schema["properties"]["schema_version"]["const"]:
        errors.append("schema_version must be 1")
    roles = data.get("roles", {})
    if not isinstance(roles, dict):
        errors.append("roles must be an object")
        return errors
    for key, value in roles.items():
        if key not in KNOWN_ROLES:
            errors.append(f"unknown role {key!r}")
        if not isinstance(value, str) or not value.strip():
            errors.append(f"role {key!r} needs a non-empty string")
        elif value.strip() in ALIAS:
            continue
    for key in ("arena_runners", "arena_cross_judge_pool", "interrogate_reviewers"):
        value = data.get(key)
        if value is None:
            continue
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            errors.append(f"{key} must be a list of non-empty strings")
    unknown = set(data) - {"schema_version", "roles", "arena_runners", "arena_cross_judge_pool", "interrogate_reviewers"}
    for key in sorted(unknown):
        errors.append(f"unknown top-level key {key!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="override file (.json or markdown with role lines)")
    args = parser.parse_args()
    try:
        data = load_override(args.path.expanduser())
    except Exception as exc:  # noqa: BLE001 - CLI surface
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"ok: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
