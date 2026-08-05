#!/usr/bin/env python3
"""Port Cursor pstack markdown to runtime-agnostic Agent Skills."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

PORTABILITY_BLOCK = """
## Portability (required)

This skill is part of the portable **pstack** pack for multiple coding agents.

1. Read `pstack` skill `references/capability-contract.md` (or this skill's `references/capability-contract.md` if present).
2. Detect the runtime and read one adapter before any delegation:
   - Cursor → `references/adapters/cursor.md` (under the `pstack` or `poteto-mode` skill)
   - Codex → `references/adapters/codex.md`
   - Anything else / unsure → `references/adapters/generic.md`
3. Translate upstream Cursor mechanics through the adapter. Do **not** invent Cursor `Task` / `poteto-agent` / model slugs on runtimes that lack them.
4. If multi-agent tools are unavailable, collapse parallel work onto the main agent and say so briefly.

Capability verbs: `explore`, `implement`, `review`, `parallel`, `ask_user`, `verify`, `model_role`.
""".strip()

CURSOR_ONLY_FRONTMATTER = {
    "disable-model-invocation",
    "mode",
    "icon",
    "color",
    "reminder",
    "is_background",
}

# Order matters: longer / more specific first.
REPLACEMENTS: list[tuple[str, str]] = [
    (
        r"`subagent_type:\s*\"?poteto-agent\"?`",
        "`implement` / `explore` helper via the active adapter (poteto-style worker if available)",
    ),
    (
        r"subagent_type:\s*[\"']poteto-agent[\"']",
        "adapter worker / explore helper (poteto-style if available)",
    ),
    (
        r"`subagent_type:\s*\"?Comment Sicko\"?`",
        "`review` helper with the Comment Sicko rubric (`pstack` → `references/agents/comment-sicko.md`)",
    ),
    (
        r"subagent_type:\s*[\"']Comment Sicko[\"']",
        "Comment Sicko review helper via adapter",
    ),
    (
        r"`subagent_type`:\s*`generalPurpose`",
        "adapter `explore` / `implement` helper",
    ),
    (
        r"subagent_type:\s*[\"']generalPurpose[\"']",
        "adapter explore/implement helper",
    ),
    (
        r"subagent_type:\s*[\"']explore[\"']",
        "adapter `explore` helper",
    ),
    (
        r"`readonly`:\s*`true`",
        "read-only (`explore`)",
    ),
    (
        r"readonly:\s*`?true`?",
        "read-only (`explore`)",
    ),
    (
        r"`run_in_background`:\s*`true`",
        "non-blocking delegation when the adapter supports it",
    ),
    (
        r"run_in_background:\s*`?true`?",
        "non-blocking delegation when supported",
    ),
    (
        r"\bAskQuestion\b",
        "`ask_user`",
    ),
    (
        r"Cursor's `/loop` command",
        "the agent's long-running / loop mechanism if available, otherwise continue autonomously",
    ),
    (
        r"Cursor's built-in for authoring SKILL\.md files",
        "your agent's skill-authoring guidance",
    ),
    (
        r"the `deslop` skill from the `cursor-team-kit` plugin \(`/deslop`\)",
        "a local deslop / cleanup pass if available; otherwise apply `unslop` + simplicity review before commit",
    ),
    (
        r"`cursor-team-kit` publishes `control-cli` \(for CLIs and TUIs\) and `control-ui` \(for browser / Electron / web UIs\)",
        "use the best available control surface for CLI/TUI or browser/UI verification in this runtime",
    ),
    (
        r"Shipping UI / IDE / CLI → the matching control skill\. `cursor-team-kit` publishes `control-cli` \(for CLIs and TUIs\) and `control-ui` \(for browser, Electron, web UIs\)\. ",
        "Shipping UI / IDE / CLI → verify on the real control surface available in this runtime. ",
    ),
    (
        r"Spawn all explorers in a single message:",
        "Spawn explorers via `parallel` + `explore` (one message if the adapter supports fan-out):",
    ),
    (
        r"spawn a single Task subagent",
        "spawn a single `explore`/`implement` helper via the adapter",
    ),
    (
        r"Spawn a single Task subagent",
        "Spawn a single `explore`/`implement` helper via the adapter",
    ),
    (
        r"\bTask subagent\b",
        "adapter helper",
    ),
    (
        r"\bTask call\b",
        "adapter delegation call",
    ),
    (
        r"every `Task` call",
        "every adapter delegation call",
    ),
    (
        r"\bTask` call",
        "adapter` delegation call",
    ),
    (
        r"via `Task`",
        "via the adapter",
    ),
    (
        r"using `Task`",
        "using the adapter",
    ),
    (
        r"\bTask tool\b",
        "delegation tool",
    ),
    (
        r"(?<![A-Za-z])Task(?![A-Za-z])",
        "adapter delegation",
    ),
]


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
            # continuation of previous kept key — only keep if last kept was not skipped
            if out and not out[-1].startswith("#SKIP#"):
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
            # Normalize name to directory name (agentskills: lowercase hyphen)
            value = line.split(":", 1)[1].strip().strip("\"'")
            # Keep directory name as canonical package name
            out.append(f"name: {skill_dir_name}")
            i += 1
            continue
        out.append(line)
        i += 1

    # Ensure license/compatibility hints
    blob = "\n".join(out)
    if "license:" not in blob:
        out.append("license: MIT")
    if "compatibility:" not in blob:
        out.append(
            "compatibility: Works with Agent Skills-compatible coding agents. Multi-agent optional; see pstack adapters."
        )
    return "\n".join(out).strip() + "\n"


def apply_replacements(body: str) -> str:
    for pattern, repl in REPLACEMENTS:
        body = re.sub(pattern, repl, body)
    return body


def ensure_portability(body: str) -> str:
    if "## Portability (required)" in body:
        return body
    # Insert after first H1 if present, else at top
    m = re.search(r"^# .+$", body, re.M)
    if m:
        insert_at = m.end()
        return body[:insert_at] + "\n\n" + PORTABILITY_BLOCK + "\n" + body[insert_at:]
    return PORTABILITY_BLOCK + "\n\n" + body


def port_skill_md(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    skill_dir_name = path.parent.name

    if fm is None:
        body = apply_replacements(original)
        body = ensure_portability(body)
        new = body
    else:
        new_fm = clean_frontmatter(fm, skill_dir_name)
        body = apply_replacements(body)
        body = ensure_portability(body.lstrip("\n"))
        new = f"---\n{new_fm}---\n\n{body.lstrip()}"

    if new != original:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def port_plain_md(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    # Skip our adapter/contract files from destructive Task word replaces if already portable
    if path.name in {"capability-contract.md", "generic.md", "cursor.md", "codex.md"}:
        return False
    if "Portability (required)" in original and path.name == "SKILL.md":
        pass
    new = apply_replacements(original)
    if new != original:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    skill_changed = 0
    md_changed = 0
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        if port_skill_md(skill_md):
            skill_changed += 1
            print(f"ported skill: {skill_md.parent.name}")
    for md in sorted(SKILLS.rglob("*.md")):
        if md.name == "SKILL.md":
            continue
        if port_plain_md(md):
            md_changed += 1
            print(f"ported md: {md.relative_to(ROOT)}")
    # Agent reference prompts
    agents = ROOT / "skills" / "pstack" / "references" / "agents"
    if agents.exists():
        for md in agents.glob("*.md"):
            if port_plain_md(md) or True:
                text = md.read_text(encoding="utf-8")
                fm, body = split_frontmatter(text)
                if fm is not None:
                    new_fm = clean_frontmatter(fm, md.stem)
                    body = apply_replacements(body)
                    body = (
                        body
                        if "## Portability" in body
                        else ensure_portability(body.lstrip("\n"))
                    )
                    md.write_text(f"---\n{new_fm}---\n\n{body.lstrip()}", encoding="utf-8")
                    print(f"ported agent ref: {md.name}")
    print(f"done. skills={skill_changed} other_md={md_changed}")


if __name__ == "__main__":
    main()
