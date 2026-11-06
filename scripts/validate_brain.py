#!/usr/bin/env python3
"""Validates the Obsidian PARA Second Brain structure, frontmatter schema, and [[wikilinks]]."""

from __future__ import annotations

import pathlib
import re
import sys

REQUIRED_DIRS = ["inbox", "projects", "areas", "resources", "archive"]
REQUIRED_NOTE_KEYS = {"id", "title", "type", "stage", "author", "created", "requirements", "issues", "prs"}
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def strip_code_blocks(text: str) -> str:
    # Strip multi-line code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Strip inline code blocks
    text = re.sub(r"`[^`]+`", "", text)
    return text


def main() -> int:
    brain_dir = pathlib.Path("brain")
    errors: list[str] = []

    for sub in REQUIRED_DIRS:
        if not (brain_dir / sub).is_dir():
            errors.append(f"Missing PARA directory: brain/{sub}/")

    for root_file in ["index.md", "log.md"]:
        if not (brain_dir / root_file).is_file():
            errors.append(f"Missing required root brain file: brain/{root_file}")

    md_files = list(brain_dir.rglob("*.md"))
    known_targets = {f.stem for f in md_files} | {
        str(f.relative_to(brain_dir).with_suffix("")) for f in md_files
    } | {"AGENTS", "brain/index", "brain/log"}

    research_notes_count = 0
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        if md_file.name.startswith("RN-"):
            research_notes_count += 1

        if md_file.name not in {"index.md", "log.md"}:
            fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            if not fm_match:
                errors.append(f"{md_file}: Missing YAML frontmatter block.")
            else:
                keys_found = {
                    line.split(":", 1)[0].strip()
                    for line in fm_match.group(1).splitlines()
                    if ":" in line and not line.startswith(" ")
                }
                missing = REQUIRED_NOTE_KEYS - keys_found
                if missing:
                    errors.append(f"{md_file}: Missing frontmatter keys {sorted(missing)}")

        clean_text = strip_code_blocks(text)
        links = WIKILINK_RE.findall(clean_text)
        if not links:
            errors.append(f"{md_file}: Contains zero [[wikilinks]] (violates SB-1).")
        for target in links:
            target_clean = target.strip()
            if target_clean not in known_targets and target_clean.split("/")[-1] not in known_targets:
                errors.append(f"{md_file}: Broken wikilink [[{target}]]")

    if research_notes_count < 10:
        errors.append(
            f"Stage 1 requires at least 10 research notes (found {research_notes_count})."
        )

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print(
        f"SUCCESS: Validated {len(md_files)} brain notes ({research_notes_count} research notes) and all [[wikilinks]]."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())