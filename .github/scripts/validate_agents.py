#!/usr/bin/env python3
"""Validate nurutech-company agent files.

For every subagent under `.claude/agents/*.md`, this script checks that:
  1. the file starts with a YAML-style frontmatter block delimited by `---`,
  2. the frontmatter declares a non-empty `name` and `description`,
  3. the declared `name` matches the file name (minus the `.md` extension),
  4. a matching design document exists at `docs/agents/<name>.md`.

The script uses only the Python standard library so it runs on a clean runner
without installing anything. It exits non-zero if any check fails.
"""

from __future__ import annotations

import sys
from pathlib import Path

AGENTS_DIR = Path(".claude/agents")
DOCS_DIR = Path("docs/agents")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return a flat dict of top-level scalar keys from a leading frontmatter block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("file does not start with a '---' frontmatter block")

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    raise ValueError("frontmatter block is not closed with '---'")


def main() -> int:
    if not AGENTS_DIR.is_dir():
        print(f"error: {AGENTS_DIR} does not exist")
        return 1

    agent_files = sorted(AGENTS_DIR.glob("*.md"))
    if not agent_files:
        print(f"error: no agent files found in {AGENTS_DIR}")
        return 1

    errors: list[str] = []
    for path in agent_files:
        text = path.read_text(encoding="utf-8")
        try:
            fm = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
            continue

        name = fm.get("name", "")
        if not name:
            errors.append(f"{path}: missing or empty 'name' in frontmatter")
        if not fm.get("description", ""):
            errors.append(f"{path}: missing or empty 'description' in frontmatter")

        expected = path.stem
        if name and name != expected:
            errors.append(
                f"{path}: frontmatter name '{name}' does not match file name '{expected}'"
            )

        if name:
            doc = DOCS_DIR / f"{name}.md"
            if not doc.is_file():
                errors.append(f"{path}: missing companion document {doc}")

    if errors:
        print("Agent validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Validated {len(agent_files)} agent file(s); all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
