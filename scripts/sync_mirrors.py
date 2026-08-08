#!/usr/bin/env python3
"""Refresh byte-identical mirrors from their canonical directories."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Shared playbook references that live beside playbooks under poteto-mode,
# but must also exist under pstack/references for /pstack relative links.
SHARED_PLAYBOOK_REFS = (
    "plan.md",
    "bugbot-triage.md",
)


def sync_dir(src: Path, dest: Path) -> None:
    if not src.is_dir():
        raise SystemExit(f"missing source directory: {src}")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main() -> int:
    sync_dir(
        ROOT / "skills" / "poteto-mode" / "playbooks",
        ROOT / "skills" / "pstack" / "playbooks",
    )
    sync_dir(
        ROOT / "skills" / "pstack" / "references" / "adapters",
        ROOT / "skills" / "poteto-mode" / "references" / "adapters",
    )
    contract_src = ROOT / "skills" / "pstack" / "references" / "capability-contract.md"
    contract_dest = ROOT / "skills" / "poteto-mode" / "references" / "capability-contract.md"
    shutil.copy2(contract_src, contract_dest)

    for name in SHARED_PLAYBOOK_REFS:
        src = ROOT / "skills" / "poteto-mode" / "references" / name
        dest = ROOT / "skills" / "pstack" / "references" / name
        if not src.is_file():
            raise SystemExit(f"missing shared reference: {src}")
        shutil.copy2(src, dest)

    for name in ("host-lifecycle.md", "workflow-quality.md"):
        src = ROOT / "skills" / "pstack" / "references" / name
        dest = ROOT / "skills" / "poteto-mode" / "references" / name
        if not src.is_file():
            raise SystemExit(f"missing shared pstack reference: {src}")
        shutil.copy2(src, dest)

    print(
        "synced playbooks, adapters, capability-contract, shared playbook references, and lifecycle docs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
