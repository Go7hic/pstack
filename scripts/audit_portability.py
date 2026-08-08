#!/usr/bin/env python3
"""Audit portable pstack's structural and vendor-neutrality invariants."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
FIXTURES = ROOT / "scripts" / "fixtures" / "portability"

PLAYBOOKS = {
    "investigation.md",
    "bug-fix.md",
    "perf-issue.md",
    "hillclimb.md",
    "runtime-forensics.md",
    "trace-forensics.md",
    "feature.md",
    "refactoring.md",
    "prototype.md",
    "visual-parity.md",
    "authoring-a-skill.md",
    "eval.md",
    "babysit.md",
    "shipping.md",
    "autonomous-run.md",
    "orchestrate.md",
    "autopilot-full.md",
    "autopilot-stack.md",
    "session-pickup.md",
    "pause-safely.md",
    "multi-phase-plan.md",
    "worktree-cleanup.md",
    "opening-a-pr.md",
}

ADAPTERS = {
    "claude-code.md",
    "codex.md",
    "codex-models.md",
    "cursor.md",
    "droid.md",
    "generic.md",
    "opencode.md",
}

FORBIDDEN_FRONTMATTER = {
    "disable-model-invocation",
    "mode",
    "icon",
    "color",
    "reminder",
    "is_background",
}

PORTABILITY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "concrete Cursor model slug",
        re.compile(
            r"\b(?:grok-4\.5-fast-xhigh|gpt-5\.6-sol-max|"
            r"claude-fable-5-thinking-max|claude-opus-5-thinking-xhigh)\b"
        ),
    ),
    ("Cursor-only subagent_type", re.compile(r"\bsubagent_type\s*:")),
    ("Cursor-only background flag", re.compile(r"\brun_in_background\s*:")),
    ("runtime-specific readonly flag", re.compile(r"\breadonly\s*:")),
    ("Cursor AskQuestion API", re.compile(r"\bAskQuestion\b")),
    (
        "Cursor filesystem path assumption",
        re.compile(r"~/\.cursor/(?:projects|skills|plugins)/"),
    ),
    ("Cursor built-in workflow", re.compile(r"Cursor(?:'s)? built-in", re.I)),
    ("cursor-team-kit dependency", re.compile(r"cursor-team-kit", re.I)),
    (
        "Cursor control-surface dependency",
        re.compile(r"\bcontrol-(?:cli|ui)\b", re.I),
    ),
    (
        "Cursor transcript directory assumption",
        re.compile(r"\bagent-transcripts\b"),
    ),
    (
        "Cursor cloud/dashboard workflow",
        re.compile(
            r"\bCursor cloud(?: agent)?\b|\bCursor dashboard\b|\bCursor restart\b",
            re.I,
        ),
    ),
    (
        "ambiguous generated helper wording",
        re.compile(r"adapter\s+`?explore`?\s*/\s*`?implement`?\s+helpers?", re.I),
    ),
    (
        "ambiguous generated model role",
        re.compile(r"model_role:fast_explore\s*/\s*feature_impl", re.I),
    ),
)

SCAN_EXCLUDES = (
    "skills/pstack/references/adapters/",
    "skills/poteto-mode/references/adapters/",
    "skills/pstack/references/agents/",
)


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str
    line: int | None = None

    def render(self) -> str:
        location = self.path if self.line is None else f"{self.path}:{self.line}"
        return f"{self.level}: {location}: {self.message}"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    return fields, text[end + 5 :]


def compare_mirror(left: Path, right: Path, findings: list[Finding]) -> None:
    label = f"{relative(left)} ↔ {relative(right)}"
    if not left.is_dir() or not right.is_dir():
        findings.append(Finding("ERROR", label, "mirror directory is missing"))
        return

    left_files = {
        path.relative_to(left).as_posix(): path
        for path in left.rglob("*")
        if path.is_file()
    }
    right_files = {
        path.relative_to(right).as_posix(): path
        for path in right.rglob("*")
        if path.is_file()
    }

    for name in sorted(left_files.keys() ^ right_files.keys()):
        side = "left only" if name in left_files else "right only"
        findings.append(Finding("ERROR", label, f"{name} exists on {side}"))

    for name in sorted(left_files.keys() & right_files.keys()):
        if left_files[name].read_bytes() != right_files[name].read_bytes():
            findings.append(Finding("ERROR", label, f"{name} has drifted"))


def check_expected_files(
    directory: Path, expected: set[str], findings: list[Finding]
) -> None:
    if not directory.is_dir():
        findings.append(Finding("ERROR", relative(directory), "directory is missing"))
        return
    actual = {path.name for path in directory.iterdir() if path.is_file()}
    for name in sorted(expected - actual):
        findings.append(Finding("ERROR", relative(directory), f"missing {name}"))
    for name in sorted(actual - expected):
        findings.append(Finding("ERROR", relative(directory), f"unexpected file {name}"))


def check_skills(findings: list[Finding]) -> None:
    if not SKILLS.is_dir():
        findings.append(Finding("ERROR", "skills", "skills directory is missing"))
        return

    seen_names: dict[str, str] = {}
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        rel = relative(path)
        try:
            fields, body = parse_frontmatter(path)
        except ValueError as exc:
            findings.append(Finding("ERROR", rel, str(exc)))
            continue

        expected_name = path.parent.name
        actual_name = fields.get("name")
        if actual_name != expected_name:
            findings.append(
                Finding(
                    "ERROR",
                    rel,
                    f"frontmatter name must be {expected_name!r}, got {actual_name!r}",
                )
            )

        for key in ("license", "compatibility"):
            if not fields.get(key):
                findings.append(Finding("ERROR", rel, f"missing frontmatter field {key!r}"))

        for key in sorted(FORBIDDEN_FRONTMATTER & fields.keys()):
            findings.append(Finding("ERROR", rel, f"Cursor-only frontmatter key {key!r}"))

        if actual_name:
            previous = seen_names.get(actual_name)
            if previous:
                findings.append(
                    Finding(
                        "ERROR",
                        rel,
                        f"duplicate skill name {actual_name!r}; also used by {previous}",
                    )
                )
            else:
                seen_names[actual_name] = rel

        if "## Portability (required)" not in body:
            findings.append(Finding("WARN", rel, "missing the standard portability block"))


def match_labels(text: str) -> set[str]:
    labels: set[str] = set()
    for label, pattern in PORTABILITY_PATTERNS:
        if pattern.search(text):
            labels.add(label)
    return labels


def check_fixtures(findings: list[Finding]) -> None:
    bad_dir = FIXTURES / "bad"
    good_dir = FIXTURES / "good"
    if not bad_dir.is_dir() or not good_dir.is_dir():
        findings.append(
            Finding("ERROR", relative(FIXTURES), "bad/ and good/ fixture directories required")
        )
        return

    bad_files = sorted(path for path in bad_dir.glob("*.md") if path.is_file())
    if not bad_files:
        findings.append(Finding("ERROR", relative(bad_dir), "expected at least one bad fixture"))

    covered_labels: set[str] = set()
    for path in bad_files:
        labels = match_labels(read_text(path))
        if not labels:
            findings.append(
                Finding(
                    "ERROR",
                    relative(path),
                    "bad fixture matched no portability pattern",
                )
            )
            continue
        covered_labels.update(labels)

    expected_labels = {label for label, _ in PORTABILITY_PATTERNS}
    for label in sorted(expected_labels - covered_labels):
        findings.append(
            Finding(
                "ERROR",
                relative(bad_dir),
                f"no bad fixture covers pattern {label!r}",
            )
        )

    good_files = sorted(path for path in good_dir.glob("*.md") if path.is_file())
    if not good_files:
        findings.append(
            Finding("ERROR", relative(good_dir), "expected at least one good fixture")
        )
    for path in good_files:
        labels = match_labels(read_text(path))
        if labels:
            findings.append(
                Finding(
                    "ERROR",
                    relative(path),
                    "good fixture matched: " + ", ".join(sorted(labels)),
                )
            )


def changed_paths(base_ref: str) -> set[str]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"git diff failed for {base_ref}")
    return {line.strip() for line in completed.stdout.splitlines() if line.strip()}


def should_scan(path: Path, selected: set[str] | None) -> bool:
    rel = relative(path)
    if selected is not None and rel not in selected:
        return False
    if path.suffix != ".md":
        return False
    if rel.startswith("skills/"):
        return not any(rel.startswith(prefix) for prefix in SCAN_EXCLUDES)
    return rel.startswith("docs/guide/")


def scan_portability(
    findings: list[Finding], selected: set[str] | None, strict: bool
) -> None:
    level = "ERROR" if strict else "WARN"
    candidates = list(SKILLS.rglob("*.md")) + list(
        (ROOT / "docs" / "guide").rglob("*.md")
    )
    for path in sorted(candidates):
        if not should_scan(path, selected):
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            for label, pattern in PORTABILITY_PATTERNS:
                if pattern.search(line):
                    findings.append(Finding(level, relative(path), label, line_number))


def run(strict: bool, changed_from: str | None) -> list[Finding]:
    findings: list[Finding] = []

    check_skills(findings)
    check_expected_files(SKILLS / "pstack" / "playbooks", PLAYBOOKS, findings)
    check_expected_files(SKILLS / "poteto-mode" / "playbooks", PLAYBOOKS, findings)
    check_expected_files(
        SKILLS / "pstack" / "references" / "adapters", ADAPTERS, findings
    )
    check_expected_files(
        SKILLS / "poteto-mode" / "references" / "adapters", ADAPTERS, findings
    )

    compare_mirror(
        SKILLS / "poteto-mode" / "playbooks",
        SKILLS / "pstack" / "playbooks",
        findings,
    )
    compare_mirror(
        SKILLS / "poteto-mode" / "references" / "adapters",
        SKILLS / "pstack" / "references" / "adapters",
        findings,
    )

    left = SKILLS / "poteto-mode" / "references" / "capability-contract.md"
    right = SKILLS / "pstack" / "references" / "capability-contract.md"
    if not left.is_file() or not right.is_file():
        findings.append(
            Finding("ERROR", "capability-contract.md", "shared reference mirror is missing")
        )
    elif left.read_bytes() != right.read_bytes():
        findings.append(
            Finding("ERROR", "capability-contract.md", "shared reference mirror has drifted")
        )

    check_fixtures(findings)

    selected = changed_paths(changed_from) if changed_from else None
    scan_portability(findings, selected=selected, strict=strict)
    return findings


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat vendor-specific portability findings as errors",
    )
    parser.add_argument(
        "--changed-from",
        metavar="REF",
        help="scan vendor-specific patterns only in files changed from REF",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    try:
        findings = run(strict=args.strict, changed_from=args.changed_from)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for finding in findings:
        print(finding.render())

    errors = sum(finding.level == "ERROR" for finding in findings)
    warnings = sum(finding.level == "WARN" for finding in findings)
    print(f"portable audit: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
