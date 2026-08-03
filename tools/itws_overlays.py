#!/usr/bin/env python3
"""Validate the ITWS profile-overlay layout defined in §1.5.

The checker consumes the normalized model in :mod:`itws.parser`. Its
command-line interface is unchanged from 0.5.1-draft.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.parser import (
    OVERLAY_DIRNAME,
    PROFILE_RULES_FILENAME,
    SHARED_DIRNAME,
    SpecError,
    parse_profiles,
    parse_skeletons,
)
from itws.vocab import PROFILE_FAMILIES, PROFILE_IDS, profile_families

REQUIRED_FILES = ("README.md", "reader.md", "skeleton.md", PROFILE_RULES_FILENAME)

REGISTRY_ROW_RE = re.compile(
    r"^\| `(?P<profile>[a-z-]+)` \| \[(?P<dir>[a-z-]+)/\]\([a-z-]+/\) \| "
    r"(?P<modules>.+?) \|$",
    re.MULTILINE,
)

#: An overlay's Annex D pointer sentence. The identifiers themselves carry
#: periods, so the list runs to the end of the line and loses its final one.
EXAMPLE_POINTER_RE = re.compile(
    r"Annex D contains \w+ `(?P<profile>[a-z-]+)` examples?: (?P<ids>[^\n]*)"
)

#: One Annex D example header and the profile line that follows it.
EXAMPLE_HEADER_RE = re.compile(r"^### Example (?P<id>D\.\d+)", re.MULTILINE)
EXAMPLE_PROFILE_RE = re.compile(r"^Profile: (?P<profiles>.+)$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    return parser.parse_args()


def check_files(overlays: Path, errors: list[str]) -> None:
    for profile in PROFILE_IDS:
        directory = overlays / profile
        if not directory.is_dir():
            errors.append(f"missing overlay directory: {directory}")
            continue
        for name in REQUIRED_FILES:
            if not (directory / name).is_file():
                errors.append(f"missing overlay file: {directory / name}")

    for family in PROFILE_FAMILIES:
        module = overlays / SHARED_DIRNAME / f"{family}.md"
        if not module.is_file():
            errors.append(f"missing shared overlay module: {module}")

    known = set(PROFILE_IDS) | {SHARED_DIRNAME}
    for entry in sorted(overlays.iterdir()):
        if entry.is_dir() and entry.name not in known:
            errors.append(f"unknown overlay directory: {entry}")


def check_registry(overlays: Path, errors: list[str]) -> None:
    registry = overlays / "README.md"
    if not registry.is_file():
        errors.append(f"missing overlay registry: {registry}")
        return

    rows = REGISTRY_ROW_RE.findall(registry.read_text(encoding="utf-8"))
    listed = tuple(row[0] for row in rows)
    if listed != PROFILE_IDS:
        errors.append(
            f"{registry}: registry rows must list every profile in canonical order"
        )
        return

    for profile, directory, modules in rows:
        if directory != profile:
            errors.append(f"{registry}: `{profile}` points at {directory}/")
        expected = profile_families(profile)
        found = tuple(sorted(set(re.findall(r"shared/([a-z-]+)\.md", modules))))
        if found != expected:
            errors.append(
                f"{registry}: `{profile}` lists modules {found or ('none',)}; "
                f"expected {expected or ('none',)}"
            )


def corpus_examples(spec_dir: Path) -> dict[str, list[str]]:
    """Map each profile to the Annex D examples that declare it."""
    corpus = spec_dir / "annexes" / "annex-d-examples-corpus.md"
    text = corpus.read_text(encoding="utf-8")
    mapping: dict[str, list[str]] = {}
    headers = list(EXAMPLE_HEADER_RE.finditer(text))
    for position, header in enumerate(headers):
        stop = (
            headers[position + 1].start()
            if position + 1 < len(headers)
            else len(text)
        )
        profile_line = EXAMPLE_PROFILE_RE.search(text, header.end(), stop)
        if profile_line is None:
            continue
        for name in (
            item.strip() for item in profile_line.group("profiles").split(",")
        ):
            mapping.setdefault(name, []).append(header.group("id"))
    return mapping


def check_example_pointers(overlays: Path, spec_dir: Path, errors: list[str]) -> None:
    """Each overlay's example pointer names exactly the Annex D examples.

    The pointer is hand-written prose about generated content, so it drifts
    the moment the corpus grows. Comparing it here turns that drift into a
    failed check rather than a stale sentence a reader has to disbelieve.
    """
    corpus = corpus_examples(spec_dir)
    for profile in PROFILE_IDS:
        readme = overlays / profile / "README.md"
        if not readme.is_file():
            continue
        match = EXAMPLE_POINTER_RE.search(readme.read_text(encoding="utf-8"))
        if match is None:
            errors.append(f"{readme}: no Annex D example pointer")
            continue
        if match.group("profile") != profile:
            errors.append(
                f"{readme}: the example pointer names profile "
                f"`{match.group('profile')}`"
            )
            continue
        raw = match.group("ids").strip().rstrip(".")
        listed = [
            item.strip()
            for item in raw.replace(", and ", ", ").replace(" and ", ", ").split(",")
            if item.strip()
        ]
        expected = corpus.get(profile, [])
        if listed != expected:
            errors.append(
                f"{readme}: the example pointer lists {listed or ['none']}; "
                f"Annex D declares {expected or ['none']}"
            )


def main() -> int:
    args = parse_args()
    overlays = args.spec_dir / OVERLAY_DIRNAME
    errors: list[str] = []

    if not overlays.is_dir():
        print(f"missing overlay directory: {overlays}", file=sys.stderr)
        return 1

    check_files(overlays, errors)
    check_registry(overlays, errors)
    check_example_pointers(overlays, args.spec_dir, errors)

    skeleton_count = 0
    try:
        parse_profiles(args.spec_dir)
        skeletons = parse_skeletons(args.spec_dir)
        skeleton_count = len(skeletons)
    except SpecError as error:
        errors.append(str(error))

    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(
        f"overlay layout is valid: {len(PROFILE_IDS)} profiles, "
        f"{len(PROFILE_FAMILIES)} shared modules, {skeleton_count} skeletons"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
