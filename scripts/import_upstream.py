#!/usr/bin/env python3
"""Import an upstream Cursor pstack checkout into this portable pack.

Usage:
  python3 scripts/import_upstream.py --upstream-root /path/to/cursor/plugins/pstack

Hand-maintained protection is file-level:
- SKILL.md files listed in UPSTREAM_MANIFEST.json portable.hand_maintained_skills are kept
- adapters, capability-contract, agents, and other local-only paths are never overwritten
- poteto-mode playbooks/references (except adapters) are still imported
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


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def protected_skill_mds(manifest: dict) -> set[str]:
    return set(manifest["portable"]["hand_maintained_skills"])


def should_skip_path(rel: str, protected_skills: set[str]) -> bool:
    if rel.startswith("skills/pstack/references/adapters/"):
        return True
    if rel.startswith("skills/poteto-mode/references/adapters/"):
        return True
    if rel in {
        "skills/pstack/references/capability-contract.md",
        "skills/poteto-mode/references/capability-contract.md",
        "skills/pstack/references/host-lifecycle.md",
        "skills/pstack/references/workflow-quality.md",
        "skills/pstack/references/model-override.schema.json",
        "skills/pstack/references/principles-summary.md",
    }:
        return True
    if rel.startswith("skills/pstack/references/agents/"):
        return True
    parts = Path(rel).parts
    if len(parts) >= 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
        if parts[1] in protected_skills:
            return True
    if parts[:2] == ("skills", "pstack"):
        # Portable pstack entry tree is local-only except playbook mirrors.
        if not rel.startswith("skills/pstack/playbooks/"):
            return True
    return False


def copy_tree_selective(src_dir: Path, dest_dir: Path, protected_skills: set[str]) -> list[str]:
    copied: list[str] = []
    for src in sorted(src_dir.rglob("*")):
        if not src.is_file():
            continue
        rel_inside = src.relative_to(src_dir).as_posix()
        dest = dest_dir / rel_inside
        repo_rel = dest.relative_to(ROOT).as_posix()
        if should_skip_path(repo_rel, protected_skills):
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(repo_rel)
    return copied


def copy_upstream_skills(upstream_root: Path, protected_skills: set[str]) -> list[str]:
    src_skills = upstream_root / "skills"
    bases = [src_skills] if src_skills.is_dir() else [upstream_root]
    copied: list[str] = []
    for base in bases:
        for skill_md in sorted(base.glob("*/SKILL.md")):
            name = skill_md.parent.name
            dest = ROOT / "skills" / name
            dest.mkdir(parents=True, exist_ok=True)
            copied.extend(copy_tree_selective(skill_md.parent, dest, protected_skills))
    return copied


def run(cmd: list[str]) -> None:
    completed = subprocess.run(cmd, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def resolve_upstream_commit(upstream_root: Path, provided: str | None) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=upstream_root,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        if provided:
            return provided
        raise SystemExit("upstream root is not a git checkout; pass --upstream-commit")
    head = completed.stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=upstream_root,
        check=False,
        text=True,
        capture_output=True,
    )
    if dirty.stdout.strip():
        raise SystemExit("upstream checkout is dirty; commit or stash before import")
    if provided and provided != head:
        raise SystemExit(f"--upstream-commit {provided} != upstream HEAD {head}")
    return head


def update_manifest(commit: str, report_path: Path) -> None:
    data = load_manifest()
    data["upstream"]["commit"] = commit
    data["upstream"]["synced_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if report_path.is_file():
        data["upstream"]["last_import_report"] = report_path.as_posix()
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

    manifest = load_manifest()
    protected = protected_skill_mds(manifest)
    commit = resolve_upstream_commit(upstream_root, args.upstream_commit)
    copied = copy_upstream_skills(upstream_root, protected)
    print(f"copied {len(copied)} files (hand-maintained paths skipped)")
    run(
        [
            sys.executable,
            str(ROOT / "scripts" / "port_to_portable.py"),
            "--report",
            str(args.report),
        ]
    )
    run([sys.executable, str(ROOT / "scripts" / "sync_mirrors.py")])
    run([sys.executable, str(ROOT / "scripts" / "audit_portability.py"), "--strict"])
    update_manifest(commit, args.report)

    checklist = ROOT / "scripts" / "fixtures" / "semantic" / "REVIEW_CHECKLIST.md"
    print("\nSemantic review checklist:")
    print(checklist.read_text(encoding="utf-8"))
    print(f"\nPinned upstream commit: {commit}")
    print(f"Transform report: {args.report}")
    print("Do not auto-merge. Open a draft PR after human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
