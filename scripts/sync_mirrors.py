#!/usr/bin/env python3
"""Refresh or verify byte-identical mirrors from their canonical directories.

Canonical sources:
- playbooks: skills/poteto-mode/playbooks
- adapters / agents / capability-contract / model-override.schema /
  host-lifecycle / workflow-quality: skills/pstack/references
- plan.md / bugbot-triage.md: skills/poteto-mode/references
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHARED_PLAYBOOK_REFS = (
    "plan.md",
    "bugbot-triage.md",
)

PSTACK_TO_POTETO_FILES = (
    "capability-contract.md",
    "host-lifecycle.md",
    "workflow-quality.md",
    "model-override.schema.json",
)


def pairs() -> list[tuple[Path, Path]]:
    items: list[tuple[Path, Path]] = []

    left = ROOT / "skills" / "poteto-mode" / "playbooks"
    right = ROOT / "skills" / "pstack" / "playbooks"
    for path in left.rglob("*"):
        if path.is_file():
            items.append((path, right / path.relative_to(left)))

    left = ROOT / "skills" / "pstack" / "references" / "adapters"
    right = ROOT / "skills" / "poteto-mode" / "references" / "adapters"
    for path in left.rglob("*"):
        if path.is_file():
            items.append((path, right / path.relative_to(left)))

    left = ROOT / "skills" / "pstack" / "references" / "agents"
    right = ROOT / "skills" / "poteto-mode" / "references" / "agents"
    for path in left.rglob("*"):
        if path.is_file():
            items.append((path, right / path.relative_to(left)))

    for name in SHARED_PLAYBOOK_REFS:
        items.append(
            (
                ROOT / "skills" / "poteto-mode" / "references" / name,
                ROOT / "skills" / "pstack" / "references" / name,
            )
        )

    for name in PSTACK_TO_POTETO_FILES:
        items.append(
            (
                ROOT / "skills" / "pstack" / "references" / name,
                ROOT / "skills" / "poteto-mode" / "references" / name,
            )
        )
    return items


def check_mirrors() -> int:
    errors = 0
    for src, dest in pairs():
        rel_src = src.relative_to(ROOT).as_posix()
        rel_dest = dest.relative_to(ROOT).as_posix()
        if not src.is_file():
            print(f"ERROR: missing canonical {rel_src}")
            errors += 1
            continue
        if not dest.is_file():
            print(f"ERROR: missing mirror {rel_dest}")
            errors += 1
            continue
        if not filecmp.cmp(src, dest, shallow=False):
            print(f"ERROR: drifted {rel_src} ↔ {rel_dest}")
            errors += 1
    print(f"mirror check: {errors} error(s)")
    return 1 if errors else 0


def sync_dir(src: Path, dest: Path) -> None:
    if not src.is_dir():
        raise SystemExit(f"missing source directory: {src}")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def apply_sync() -> int:
    sync_dir(
        ROOT / "skills" / "poteto-mode" / "playbooks",
        ROOT / "skills" / "pstack" / "playbooks",
    )
    sync_dir(
        ROOT / "skills" / "pstack" / "references" / "adapters",
        ROOT / "skills" / "poteto-mode" / "references" / "adapters",
    )
    sync_dir(
        ROOT / "skills" / "pstack" / "references" / "agents",
        ROOT / "skills" / "poteto-mode" / "references" / "agents",
    )

    for name in SHARED_PLAYBOOK_REFS:
        src = ROOT / "skills" / "poteto-mode" / "references" / name
        dest = ROOT / "skills" / "pstack" / "references" / name
        if not src.is_file():
            raise SystemExit(f"missing shared reference: {src}")
        shutil.copy2(src, dest)

    for name in PSTACK_TO_POTETO_FILES:
        src = ROOT / "skills" / "pstack" / "references" / name
        dest = ROOT / "skills" / "poteto-mode" / "references" / name
        if not src.is_file():
            raise SystemExit(f"missing shared pstack reference: {src}")
        shutil.copy2(src, dest)

    print(
        "synced playbooks, adapters, agents, capability-contract, "
        "model-override schema, shared refs, and lifecycle docs"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify mirrors without writing; fail on drift or missing files",
    )
    args = parser.parse_args()
    return check_mirrors() if args.check else apply_sync()


if __name__ == "__main__":
    raise SystemExit(main())
