#!/usr/bin/env python3
"""Second-pass portable cleanups: models, cursor paths, leftover Task phrasing."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

REPLACEMENTS: list[tuple[str, str]] = [
    (
        r"~/\.cursor/rules/pstack-models\.mdc",
        "the local pstack model override file (Cursor: `~/.cursor/rules/pstack-models.mdc`; Codex: `~/.codex/rules/pstack-models.md`; else adapter defaults)",
    ),
    (
        r"`control-cli` or `control-ui` from `cursor-team-kit` as the change demands",
        "the real CLI/TUI or browser/UI surface available in this runtime",
    ),
    (
        r"via the control skill",
        "on the matching real surface",
    ),
    (
        r"`control-cli` or `control-ui`",
        "the matching CLI/UI control surface",
    ),
    (
        r"from `cursor-team-kit`",
        "if available in this environment",
    ),
    (
        r"cursor-team-kit",
        "optional local control/deslop tooling",
    ),
    (
        r"`subagent_type:\s*generalPurpose`",
        "adapter `explore`/`implement` helpers",
    ),
    (
        r"subagent_type:\s*generalPurpose",
        "adapter explore/implement helpers",
    ),
    (
        r"`environment:\s*\"cloud\"`",
        "isolated/cloud worker environment when the adapter supports it",
    ),
    (
        r"environment:\s*\"cloud\"",
        "isolated/cloud worker environment when supported",
    ),
    (
        r"`environment:\s*\"local\"`",
        "local worker environment when the adapter supports it",
    ),
    (
        r"environment:\s*\"local\"",
        "local worker environment when supported",
    ),
    (
        r"`adapter delegation`",
        "adapter delegation",
    ),
    (
        r"One message, three `adapter` delegation calls",
        "One message, three adapter delegation calls",
    ),
    (
        r"Spawn `adapter delegation` with",
        "Spawn via adapter with",
    ),
    (
        r"/loop`",
        "long-run/loop`",
    ),
    (
        r"`/loop`",
        "long-run/loop",
    ),
    (
        r"/loop\b",
        "long-run/loop",
    ),
    # Model defaults → role names (keep slug in parentheses as Cursor example only once patterns)
    (
        r"default `grok-4\.5-fast-xhigh`",
        "default `model_role:fast_explore` / feature_impl (Cursor example: grok-4.5-fast-xhigh)",
    ),
    (
        r"default `gpt-5\.6-sol-max`",
        "default `model_role:bug_impl` / judgment (Cursor example: gpt-5.6-sol-max)",
    ),
    (
        r"default `claude-fable-5-thinking-max`",
        "default `model_role:judgment` (Cursor example: claude-fable-5-thinking-max)",
    ),
    (
        r"your configured feature model \(default `model_role:fast_explore` / feature_impl \(Cursor example: grok-4\.5-fast-xhigh\)\)",
        "your configured feature model (`model_role:feature_impl`)",
    ),
    (
        r"your configured refactoring model \(default `model_role:fast_explore` / feature_impl \(Cursor example: grok-4\.5-fast-xhigh\)\)",
        "your configured refactoring model (`model_role:feature_impl`)",
    ),
    (
        r"your configured bug-fix model \(default `model_role:bug_impl` / judgment \(Cursor example: gpt-5\.6-sol-max\)\)",
        "your configured bug-fix model (`model_role:bug_impl`)",
    ),
    (
        r"Otherwise default to one each on `claude-fable-5-thinking-max`, `gpt-5\.6-sol-max`, `grok-4\.5-fast-xhigh`, `claude-opus-5-thinking-xhigh`",
        "Otherwise default to diverse `model_role:critic` / judgment runners across available model families",
    ),
    (
        r"Otherwise use `claude-fable-5-thinking-max`, `gpt-5\.6-sol-max`, `grok-4\.5-fast-xhigh`, `claude-opus-5-thinking-xhigh`",
        "Otherwise use diverse available judgment/critic models via `model_role`",
    ),
    (
        r"Otherwise use `grok-4\.5-fast-xhigh`",
        "Otherwise use `model_role:fast_explore`",
    ),
    (
        r"\(default `grok-4\.5-fast-xhigh`\)",
        "(`model_role:fast_explore`)",
    ),
    (
        r"\(default `gpt-5\.6-sol-max`\)",
        "(`model_role:bug_impl`)",
    ),
    (
        r"\(default `claude-fable-5-thinking-max`\)",
        "(`model_role:judgment`)",
    ),
]


ROLE_TABLE_NOTE = """
## Model roles

Do not hard-require Cursor model slugs. Resolve models through `model_role` and the active adapter:

| Role | Use |
| --- | --- |
| `fast_explore` | Broad read-only fan-out, mechanical edits |
| `feature_impl` | Spec-driven implementation / refactoring |
| `bug_impl` | High-stakes fixes after evidence |
| `judgment` | Architecture, synthesis, prose |
| `critic` | Adversarial / panel review |

If a local override file exists, prefer it. If a slug is unavailable, fall back to the parent model and say so.
""".strip()


def patch_setup_pstack(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    # Soften the defaults block to role-oriented
    text2 = re.sub(
        r"(?s)(## Defaults.*?)(?=\n## |\n# |\Z)",
        """## Defaults

Write role → model mappings using whatever slugs the current agent exposes. Example shape (values are illustrative):

```text
feature, refactoring: <fast_code_model>
bug-fix, perf-issue, hillclimb: <strong_reasoning_model>
judgment and prose: <strong_judgment_model>
hardest tasks: <strong_judgment_or_instruction_model>
how explorer: <fast_explore_model>
how explainer: <judgment_model>
how critics: <diverse judgment panel>
why investigators: <fast_explore_model>
why synthesizer: <judgment_model>
reflect tooling: <balanced_model>
reflect judgment, divergent, synthesizer: <judgment_model>
arena runners: <diverse panel>
arena cross-judge pool: <diverse panel>
swarm workers: <fast_explore_model>
architect runners: <diverse panel>
interrogate reviewers: <diverse panel>
```

Prefer writing the override beside the active agent (see Portability adapters). Do not assume Cursor-only paths.

""",
        text,
        count=1,
    )
    if text2 == text:
        # try alternate heading
        if "Model roles" not in text:
            text2 = text.rstrip() + "\n\n" + ROLE_TABLE_NOTE + "\n"
    path.write_text(text2, encoding="utf-8")


def main() -> None:
    changed = 0
    for md in sorted(SKILLS.rglob("*.md")):
        original = md.read_text(encoding="utf-8")
        new = original
        for pattern, repl in REPLACEMENTS:
            new = re.sub(pattern, repl, new)
        if md.name == "SKILL.md" and md.parent.name in {
            "how",
            "why",
            "architect",
            "arena",
            "swarm",
            "interrogate",
            "reflect",
            "setup-pstack",
            "poteto-mode",
            "pstack",
        }:
            if "## Model roles" not in new and "model_role" in new or md.parent.name in {
                "arena",
                "swarm",
                "interrogate",
                "how",
                "setup-pstack",
            }:
                if "## Model roles" not in new:
                    # append once before end
                    new = new.rstrip() + "\n\n" + ROLE_TABLE_NOTE + "\n"
        if new != original:
            md.write_text(new, encoding="utf-8")
            changed += 1
            print(f"cleaned: {md.relative_to(ROOT)}")
    patch_setup_pstack(SKILLS / "setup-pstack" / "SKILL.md")
    print(f"setup-pstack patched; files_changed={changed}")


if __name__ == "__main__":
    main()
