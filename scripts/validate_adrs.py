"""Validates Architecture Decision Records in docs/adr/ (SE-3, SB-3).

Rules:
  * file name is NNNN-kebab-case-title.md and the H1 is "# ADR-NNNN: <title>"
  * NNNN in the file name equals NNNN in the H1; numbers are unique
  * "- Status:" is Proposed, Accepted, Deprecated or Superseded; "- Date:" is YYYY-MM-DD
  * sections Context, Decision, Consequences and Brain Citations are present
  * the Brain Citations section holds at least one [[wikilink]] to an existing brain note
If docs/adr/ has no ADRs yet the script reports that and exits 0.
"""

from __future__ import annotations

import pathlib
import re
import sys

ADR_DIR = pathlib.Path("docs/adr")
BRAIN_DIR = pathlib.Path("brain")
FILENAME_RE = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
TITLE_RE = re.compile(r"^# ADR-(\d{4}): .+$", re.MULTILINE)
STATUS_RE = re.compile(r"^- Status: (Proposed|Accepted|Deprecated|Superseded)\b", re.MULTILINE)
DATE_RE = re.compile(r"^- Date: \d{4}-\d{2}-\d{2}\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
REQUIRED_HEADINGS = ("## Context", "## Decision", "## Consequences", "## Brain Citations")


def brain_stems() -> set[str]:
    return {path.stem for path in BRAIN_DIR.rglob("*.md")}


def citations_section(text: str) -> str:
    marker = "## Brain Citations"
    start = text.find(marker)
    if start == -1:
        return ""
    rest = text[start + len(marker):]
    next_heading = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: next_heading.start()] if next_heading else rest


def validate_adr(path: pathlib.Path, stems: set[str]) -> list[str]:
    errors: list[str] = []
    name_match = FILENAME_RE.match(path.name)
    if not name_match:
        return [f"{path}: file name must match NNNN-kebab-case-title.md"]
    text = path.read_text(encoding="utf-8")
    title_match = TITLE_RE.search(text)
    if not title_match:
        errors.append(f"{path}: missing H1 of the form '# ADR-NNNN: <title>'")
    elif title_match.group(1) != name_match.group(1):
        errors.append(f"{path}: H1 number {title_match.group(1)} != file number")
    if not STATUS_RE.search(text):
        errors.append(f"{path}: missing '- Status: Proposed|Accepted|Deprecated|Superseded'")
    if not DATE_RE.search(text):
        errors.append(f"{path}: missing '- Date: YYYY-MM-DD'")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"{path}: missing section '{heading}'")
    links = [t.strip() for t in WIKILINK_RE.findall(citations_section(text))]
    if not links:
        errors.append(f"{path}: Brain Citations must cite at least one [[note]] (SB-3)")
    for target in links:
        if target.split("/")[-1] not in stems:
            errors.append(f"{path}: cited brain note [[{target}]] does not exist")
    return errors


def main() -> int:
    adr_files = sorted(p for p in ADR_DIR.glob("*.md") if p.name.lower() != "readme.md")
    if not adr_files:
        print("NOTICE: no ADRs found in docs/adr/ yet; nothing to validate.")
        return 0
    stems = brain_stems()
    errors: list[str] = []
    seen: dict[str, pathlib.Path] = {}
    for adr in adr_files:
        errors.extend(validate_adr(adr, stems))
        number = adr.name[:4]
        if number in seen:
            errors.append(f"{adr}: duplicate ADR number also used by {seen[number]}")
        seen[number] = adr
    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1
    print(f"SUCCESS: Validated {len(adr_files)} ADR(s) and their brain citations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
