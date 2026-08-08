#!/usr/bin/env python3
"""Import an upstream Cursor pstack checkout into this portable pack.

Usage:
  python3 scripts/import_upstream.py --upstream-root /path/to/cursor/plugins/pstack

The importer copies skill markdown, runs both portable passes, refreshes mirrors,
writes a transform report, and prints a semantic-review checklist. It never
auto-commits and never overwrites hand-maintained entry skills or adapters.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "UPSTREAM_MANIFEST.json"

HAND_MAINTAINED = set(
    json.loads(MANIFEST.read_text(encoding="utf-8"))["portable"]["hand_maintained_skills"]
)


def copy_upstream_skills(upstream_root: Path) -> list[str]:
    src_skills = upstream_root / "skills"
    if not src_skills.is_dir():
        # Cursor plugin layout may keep skills at repo root of the pstack plugin.
        candidates = [upstream_root]
    else:
        candidates = [src_skills]

    copied: list[str] = []
    for base in candidates:
        for skill_md in sorted(base.glob("*/SKILL.md")):
            name = skill_md.parent.name
            if name in HAND_MAINTAINED:
                continue
            dest = ROOT / "skills" / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(skill_md.parent, dest)
            copied.append(name)
    return copied


def run(cmd: list[str]) -> None:
    completed = subprocess.run(cmd, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def update_manifest(commit: str | None) -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["upstream"]["synced_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if commit:
        data["upstream"]["commit"] = commit
    MANIFEST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--upstream-commit", default=None)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "scripts" / "fixtures" / "last-import-report.json",
    )
    args = parser.parse_args()
    upstream_root = args.upstream_root.expanduser().resolve()
    if not upstream_root.exists():
        print(f"ERROR: upstream root missing: {upstream_root}", file=sys.stderr)
        return 2

    copied = copy_upstream_skills(upstream_root)
    print(f"copied {len(copied)} upstream skill directories (hand-maintained skipped)")
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "port_to_portable.py"),
            "--report",
            str(args.report),
        ]
    )
    run([sys.executable, str(ROOT / "scripts" / "sync_mirrors.py")])
    update_manifest(args.upstream_commit)

    checklist = ROOT / "scripts" / "fixtures" / "semantic" / "REVIEW_CHECKLIST.md"
    print("\nSemantic review checklist:")
    print(checklist.read_text(encoding="utf-8"))
    print(f"\nTransform report: {args.report}")
    print("Do not auto-merge. Open a draft PR after human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
