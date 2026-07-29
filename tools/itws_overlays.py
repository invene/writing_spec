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
from itws.vocab import MINIMUM_TIER, PROFILE_FAMILIES, PROFILE_IDS, profile_families

REQUIRED_FILES = ("README.md", "reader.md", "skeleton.md", PROFILE_RULES_FILENAME)

REGISTRY_ROW_RE = re.compile(
    r"^\| `(?P<profile>[a-z-]+)` \| \[(?P<dir>[a-z-]+)/\]\([a-z-]+/\) \| "
    r"`(?P<tier>core|reviewed|publication)` \| (?P<modules>.+?) \|$",
    re.MULTILINE,
)


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

    for profile, directory, tier, modules in rows:
        if directory != profile:
            errors.append(f"{registry}: `{profile}` points at {directory}/")
        if tier != MINIMUM_TIER[profile]:
            errors.append(
                f"{registry}: `{profile}` records tier {tier}; §0.4.3 "
                f"requires {MINIMUM_TIER[profile]}"
            )
        expected = profile_families(profile)
        found = tuple(sorted(set(re.findall(r"shared/([a-z-]+)\.md", modules))))
        if found != expected:
            errors.append(
                f"{registry}: `{profile}` lists modules {found or ('none',)}; "
                f"expected {expected or ('none',)}"
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
