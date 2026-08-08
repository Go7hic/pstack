#!/usr/bin/env python3
"""Import upstream Cursor pstack markdown into portable Agent Skills form.

This pass is intentionally conservative. It never performs a bare-word ``Task``
replacement. Hand-maintained entry skills and adapters are skipped. Run
``scripts/port_pass2.py`` afterward, then ``scripts/audit_portability.py``.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MANIFEST = ROOT / "UPSTREAM_MANIFEST.json"

PORTABILITY_BLOCK = """
## Portability (required)

This skill is part of the portable **pstack** pack.

1. Read the `pstack` capability contract and the adapter for the active coding agent before any helper delegation.
2. Prefer capability verbs (`explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`) over vendor tool names.
3. Resolve models through `model_role`. Never require a vendor-specific model identifier.
4. When helper spawning is unavailable, run the work on the lead agent and state that fan-out was collapsed.
""".strip()

CURSOR_ONLY_FRONTMATTER = {
    "disable-model-invocation",
    "mode",
    "icon",
    "color",
    "reminder",
    "is_background",
}


def load_hand_maintained_skills() -> set[str]:
    if MANIFEST.is_file():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        return set(data["portable"]["hand_maintained_skills"])
    return set()


HAND_MAINTAINED_SKILLS = load_hand_maintained_skills()

HAND_MAINTAINED_PATH_PREFIXES = (
    "skills/pstack/references/adapters/",
    "skills/poteto-mode/references/adapters/",
    "skills/pstack/references/capability-contract.md",
    "skills/poteto-mode/references/capability-contract.md",
    "skills/pstack/references/agents/",
    "skills/pstack/references/model-override.schema.json",
    "skills/pstack/references/host-lifecycle.md",
    "skills/pstack/references/workflow-quality.md",
)

# Targeted phrase transforms only. Order: longer / more specific first.
REPLACEMENTS: tuple[tuple[str, str, str], ...] = (
    (
        "poteto-agent-subagent",
        r"`subagent_type:\s*\"?poteto-agent\"?`",
        "an `implement` helper using the Poteto worker rubric",
    ),
    (
        "comment-sicko-subagent",
        r"`subagent_type:\s*\"?Comment Sicko\"?`",
        "a `review` helper using the Comment Sicko rubric",
    ),
    (
        "generalPurpose-subagent",
        r"`?subagent_type`?\s*:\s*[\"']?generalPurpose[\"']?",
        "a helper selected by the active adapter",
    ),
    (
        "explore-subagent",
        r"`?subagent_type`?\s*:\s*[\"']?explore[\"']?",
        "an `explore` helper selected by the active adapter",
    ),
    (
        "readonly-true",
        r"`?readonly`?\s*:\s*`?true`?",
        "read-only intent enforced by the adapter and prompt",
    ),
    (
        "run-in-background-true",
        r"`?run_in_background`?\s*:\s*`?true`?",
        "non-blocking delegation when the active adapter supports it",
    ),
    ("ask-question", r"\bAskQuestion\b", "`ask_user`"),
    (
        "cursor-loop",
        r"Cursor's `/loop` command",
        "the host's long-running or loop mechanism when available",
    ),
    (
        "slash-loop",
        r"`/loop`",
        "the host's long-running or loop mechanism",
    ),
    (
        "cursor-skill-authoring",
        r"Cursor's built-in for authoring SKILL\.md files",
        "the active coding agent's skill-authoring workflow",
    ),
    (
        "deslop-plugin",
        r"the `deslop` skill from the `cursor-team-kit` plugin \(`/deslop`\)",
        "a local simplicity and cleanup pass, followed by `unslop` for prose",
    ),
    (
        "control-surface-pair",
        r"`control-cli` or `control-ui`(?: from `cursor-team-kit`)?",
        "the real CLI, browser, UI, or runtime surface available through `verify`",
    ),
)


@dataclass
class Transform:
    path: str
    rule: str
    count: int


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_hand_maintained(path: Path) -> bool:
    rel = relative(path)
    if path.name == "SKILL.md" and path.parent.name in HAND_MAINTAINED_SKILLS:
        return True
    return any(rel.startswith(prefix) or rel == prefix.rstrip("/") for prefix in HAND_MAINTAINED_PATH_PREFIXES)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def clean_frontmatter(fm: str, skill_dir_name: str) -> str:
    lines = fm.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            out.append(line)
            i += 1
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if out:
                out.append(line)
            i += 1
            continue
        key = line.split(":", 1)[0].strip()
        if key in CURSOR_ONLY_FRONTMATTER:
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                i += 1
            continue
        if key == "name":
            out.append(f"name: {skill_dir_name}")
            i += 1
            continue
        out.append(line)
        i += 1

    blob = "\n".join(out)
    if "license:" not in blob:
        out.append("license: MIT")
    if "compatibility:" not in blob:
        out.append(
            "compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters."
        )
    return "\n".join(out).strip() + "\n"


def apply_replacements(body: str, path: Path, report: list[Transform]) -> str:
    for rule, pattern, repl in REPLACEMENTS:
        new_body, count = re.subn(pattern, repl, body)
        if count:
            report.append(Transform(relative(path), rule, count))
            body = new_body
    return body


def ensure_portability(body: str) -> str:
    if "## Portability (required)" in body:
        return body
    match = re.search(r"^# .+$", body, re.M)
    if match:
        insert_at = match.end()
        return body[:insert_at] + "\n\n" + PORTABILITY_BLOCK + "\n" + body[insert_at:]
    return PORTABILITY_BLOCK + "\n\n" + body


def port_skill_md(path: Path, report: list[Transform], write: bool) -> bool:
    if is_hand_maintained(path):
        return False
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    skill_dir_name = path.parent.name
    if fm is None:
        body = apply_replacements(original, path, report)
        body = ensure_portability(body)
        new = body
    else:
        new_fm = clean_frontmatter(fm, skill_dir_name)
        body = apply_replacements(body, path, report)
        body = ensure_portability(body.lstrip("\n"))
        new = f"---\n{new_fm}---\n\n{body.lstrip()}"
    if new == original:
        return False
    if write:
        path.write_text(new, encoding="utf-8")
    return True


def port_plain_md(path: Path, report: list[Transform], write: bool) -> bool:
    if is_hand_maintained(path):
        return False
    if path.name in {"capability-contract.md", "host-lifecycle.md"}:
        return False
    if "references/adapters/" in relative(path):
        return False
    original = path.read_text(encoding="utf-8")
    new = apply_replacements(original, path, report)
    if new == original:
        return False
    if write:
        path.write_text(new, encoding="utf-8")
    return True


def collect_targets() -> list[Path]:
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    others = sorted(
        path
        for path in SKILLS.rglob("*.md")
        if path.name != "SKILL.md" and path.is_file()
    )
    return skills + others


def run_port(write: bool) -> tuple[list[str], list[Transform]]:
    changed: list[str] = []
    report: list[Transform] = []
    for path in collect_targets():
        if path.name == "SKILL.md":
            did = port_skill_md(path, report, write=write)
        else:
            did = port_plain_md(path, report, write=write)
        if did:
            changed.append(relative(path))
    return changed, report


def run_audit() -> int:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_portability.py"), "--strict"],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report transforms without writing files",
    )
    parser.add_argument(
        "--check-idempotent",
        action="store_true",
        help="copy skills to a temp tree, apply once, and fail if a second pass still changes files (never writes the real workspace)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="write a machine-readable JSON transform report",
    )
    parser.add_argument(
        "--skip-audit",
        action="store_true",
        help="do not run the strict portability audit after writing",
    )
    return parser.parse_args(list(argv))


def check_idempotent_in_temp() -> tuple[list[str], list[Transform], list[str]]:
    """Apply porting in a temporary skills tree. Real workspace stays untouched."""
    global SKILLS, ROOT
    original_skills = SKILLS
    original_root = ROOT
    with tempfile.TemporaryDirectory(prefix="pstack-port-idempotent-") as tmp:
        tmp_root = Path(tmp)
        tmp_skills = tmp_root / "skills"
        shutil.copytree(original_skills, tmp_skills)
        SKILLS = tmp_skills
        ROOT = tmp_root
        try:
            first, first_report = run_port(write=True)
            second, _second_report = run_port(write=False)
        finally:
            SKILLS = original_skills
            ROOT = original_root
        return first, first_report, second


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)

    if args.check_idempotent:
        first, report, second = check_idempotent_in_temp()
        if second:
            print("ERROR: import pipeline is not idempotent", file=sys.stderr)
            for path in second:
                print(f"  would change again: {path}", file=sys.stderr)
            if args.report:
                args.report.write_text(
                    json.dumps(
                        {
                            "first_pass_changed": first,
                            "second_pass_changed": second,
                            "transforms": [asdict(item) for item in report],
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
            return 1
        print(
            f"idempotent: temp apply changed {len(first)} file(s); second pass would change 0"
        )
        if args.report:
            args.report.write_text(
                json.dumps(
                    {
                        "first_pass_changed": first,
                        "second_pass_changed": [],
                        "transforms": [asdict(item) for item in report],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        return 0

    write = not args.dry_run
    changed, report = run_port(write=write)

    payload = {
        "changed": changed,
        "transforms": [asdict(item) for item in report],
    }
    if args.report:
        args.report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"port_to_portable: {len(changed)} file(s) changed, {len(report)} transform(s)")
    for path in changed:
        print(f"  {path}")

    if write and not args.skip_audit:
        pass2 = ROOT / "scripts" / "port_pass2.py"
        if pass2.is_file():
            subprocess.run([sys.executable, str(pass2)], cwd=ROOT, check=False)
        code = run_audit()
        if code != 0:
            print("ERROR: strict audit failed after import", file=sys.stderr)
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
