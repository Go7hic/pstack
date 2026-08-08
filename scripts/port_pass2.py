#!/usr/bin/env python3
"""Apply targeted second-pass cleanups after importing upstream pstack skills.

This pass is intentionally conservative. It removes known runtime-specific phrases,
but it does not claim that regex replacement is a semantic port. Run
``scripts/audit_portability.py`` and review every changed skill afterward.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

SKIP_PREFIXES = (
    "skills/pstack/references/adapters/",
    "skills/poteto-mode/references/adapters/",
    "skills/pstack/references/agents/",
)

REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"~/\.cursor/rules/pstack-models\.mdc"),
        "the model override file selected by the active adapter",
    ),
    (
        re.compile(r"Cursor's `/loop` command", re.I),
        "the host's long-running or loop mechanism when available",
    ),
    (
        re.compile(r"`/loop`"),
        "the host's long-running or loop mechanism",
    ),
    (
        re.compile(r"\bAskQuestion\b"),
        "`ask_user`",
    ),
    (
        re.compile(r"`control-cli` or `control-ui`(?: from `cursor-team-kit`)?", re.I),
        "the real CLI, browser, UI, or runtime surface available through `verify`",
    ),
    (
        re.compile(
            r"the `deslop` skill from the `cursor-team-kit` plugin \(`/deslop`\)",
            re.I,
        ),
        "a local simplicity and cleanup pass, followed by `unslop` for prose",
    ),
    (
        re.compile(r"Cursor's built-in for authoring SKILL\.md files", re.I),
        "the active coding agent's skill-authoring workflow",
    ),
    (
        re.compile(r"`subagent_type:\s*[\"']?poteto-agent[\"']?`?", re.I),
        "an `implement` helper using the Poteto worker rubric",
    ),
    (
        re.compile(r"`subagent_type:\s*[\"']?Comment Sicko[\"']?`?", re.I),
        "a `review` helper using the Comment Sicko rubric",
    ),
    (
        re.compile(r"`?subagent_type`?\s*:\s*[\"']?generalPurpose[\"']?", re.I),
        "a helper selected by the active adapter",
    ),
    (
        re.compile(r"`?subagent_type`?\s*:\s*[\"']?explore[\"']?", re.I),
        "an `explore` helper selected by the active adapter",
    ),
    (
        re.compile(r"`?run_in_background`?\s*:\s*`?true`?", re.I),
        "non-blocking delegation when the active adapter supports it",
    ),
    (
        re.compile(r"`?readonly`?\s*:\s*`?true`?", re.I),
        "read-only intent enforced by the adapter and prompt",
    ),
    (
        re.compile(r"your configured feature model \(default `grok-4\.5-fast-xhigh`\)"),
        "your configured feature model (`model_role:feature_impl`)",
    ),
    (
        re.compile(
            r"your configured refactoring model \(default `grok-4\.5-fast-xhigh`\)"
        ),
        "your configured refactoring model (`model_role:feature_impl`)",
    ),
    (
        re.compile(r"your configured bug-fix model \(default `gpt-5\.6-sol-max`\)"),
        "your configured bug-fix model (`model_role:bug_impl`)",
    ),
    (
        re.compile(r"your configured perf-issue model \(default `gpt-5\.6-sol-max`\)"),
        "your configured performance model (`model_role:bug_impl`)",
    ),
    (
        re.compile(r"your configured hillclimb model \(default `gpt-5\.6-sol-max`\)"),
        "your configured hillclimb model (`model_role:bug_impl`)",
    ),
    (
        re.compile(r"your configured how-explorer model \(default `grok-4\.5-fast-xhigh`\)"),
        "your configured How explorer (`model_role:fast_explore`)",
    ),
    (
        re.compile(
            r"your configured how-explainer model \(default `claude-fable-5-thinking-max`\)"
        ),
        "your configured How synthesizer (`model_role:judgment`)",
    ),
    (
        re.compile(
            r"your configured why-investigators model \(default `grok-4\.5-fast-xhigh`\)"
        ),
        "your configured Why investigator (`model_role:fast_explore`)",
    ),
    (
        re.compile(
            r"your configured why-synthesizer model \(default `claude-fable-5-thinking-max`\)"
        ),
        "your configured Why synthesizer (`model_role:judgment`)",
    ),
    (
        re.compile(
            r"defaults? `claude-fable-5-thinking-max`, `gpt-5\.6-sol-max`, "
            r"`grok-4\.5-fast-xhigh`, `claude-opus-5-thinking-xhigh`",
            re.I,
        ),
        "defaults to a diverse panel resolved through `model_role:critic` and `model_role:judgment`",
    ),
    (
        re.compile(
            r"Otherwise default to one each on `claude-fable-5-thinking-max`, "
            r"`gpt-5\.6-sol-max`, `grok-4\.5-fast-xhigh`, "
            r"`claude-opus-5-thinking-xhigh`",
            re.I,
        ),
        "Otherwise use a diverse panel resolved through `model_role:critic` and `model_role:judgment`",
    ),
)

ROLE_TABLE = """
## Model roles

Resolve concrete models through the active adapter and optional override file:

| Role | Use |
| --- | --- |
| `fast_explore` | broad read-only investigation and mechanical work |
| `feature_impl` | spec-driven implementation and refactoring |
| `bug_impl` | evidence-backed bug, performance, and reliability fixes |
| `judgment` | architecture, synthesis, and prose |
| `critic` | independent candidates and adversarial review |

When the host cannot select child models, inherit the parent session model.
""".strip()

ROLE_SKILLS = {
    "how",
    "why",
    "architect",
    "arena",
    "swarm",
    "interrogate",
    "reflect",
    "poteto-mode",
}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    rel = relative(path)
    return any(rel.startswith(prefix) for prefix in SKIP_PREFIXES)


def clean(text: str) -> str:
    result = text
    for pattern, replacement in REPLACEMENTS:
        result = pattern.sub(replacement, result)
    return result


def main() -> None:
    changed = 0
    for path in sorted(SKILLS.rglob("*.md")):
        if should_skip(path):
            continue

        original = path.read_text(encoding="utf-8")
        updated = clean(original)

        if (
            path.name == "SKILL.md"
            and path.parent.name in ROLE_SKILLS
            and "model_role" in updated
            and "## Model roles" not in updated
        ):
            updated = updated.rstrip() + "\n\n" + ROLE_TABLE + "\n"

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"cleaned: {relative(path)}")

    print(f"files_changed={changed}")
    print("next: python3 scripts/audit_portability.py")
    print("then review every changed skill for semantic correctness")


if __name__ == "__main__":
    main()
