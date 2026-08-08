#!/usr/bin/env python3
"""Refresh byte-identical mirrors from their canonical directories."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
    print("synced playbooks, adapters, and capability-contract mirrors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
