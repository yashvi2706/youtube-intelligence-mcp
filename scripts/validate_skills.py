#!/usr/bin/env python3
"""Validates all .skills/*/SKILL.md files for frontmatter schema, naming, and SB-3 brain citations."""

from __future__ import annotations

import pathlib
import re
import sys

REQUIRED_KEYS = {"name", "description", "version", "cited_notes"}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    block = match.group(1)
    data: dict[str, str] = {}
    current_key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if not line.startswith(" ") and ":" in line:
            key, val = line.split(":", 1)
            current_key = key.strip()
            data[current_key] = val.strip()
        elif current_key and line.strip().startswith("-"):
            data[current_key] += " " + line.strip()
    return data


def main() -> int:
    skills_dir = pathlib.Path(".skills")
    if not skills_dir.exists():
        print("ERROR: .skills/ directory does not exist.")
        return 1

    skill_files = list(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR: No SKILL.md files found under .skills/*/")
        return 1

    errors: list[str] = []
    for skill_file in skill_files:
        folder_name = skill_file.parent.name
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        missing = REQUIRED_KEYS - set(fm.keys())
        if missing:
            errors.append(f"{skill_file}: Missing frontmatter keys: {sorted(missing)}")
            continue
        if fm["name"].strip("\"'") != folder_name:
            errors.append(
                f"{skill_file}: Frontmatter name '{fm['name']}' does not match folder '{folder_name}'"
            )
        if "[[" not in fm["cited_notes"]:
            errors.append(
                f"{skill_file}: Must cite at least one distilled brain note via [[wikilink]] (SB-3)"
            )

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print(f"SUCCESS: Validated {len(skill_files)} skill(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())