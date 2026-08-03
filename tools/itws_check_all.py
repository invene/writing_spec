#!/usr/bin/env python3
"""Run every ITWS repository check in one command.

The default path is language-only. It creates no assurance bundle and passes
no review, tier, waiver, or evidence input to validation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from itws.parser import SpecError, parse_specification
from itws.vocab import PROFILE_IDS, PROFILE_SURFACES


@dataclass
class Step:
    name: str
    command: str
    passed: bool
    detail: str = ""


def run_command(name: str, args: list[str], cwd: Path) -> Step:
    process = subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    detail = (process.stdout + process.stderr).strip()
    return Step(
        name=name,
        command="python3 " + " ".join(args),
        passed=process.returncode == 0,
        detail="" if process.returncode == 0 else detail,
    )


def run_validation(
    name: str,
    args: list[str],
    root: Path,
    wanted: tuple[str, ...],
) -> Step:
    command = "python3 " + " ".join(args)
    process = subprocess.run(
        [sys.executable, *args, "--json"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(process.stdout)
        result = payload["result"]
    except (ValueError, KeyError):
        detail = (process.stdout + process.stderr).strip()
        return Step(name, command, False, detail or "no result was reported")
    reasons = "; ".join(payload.get("reasons", []))
    return Step(
        name,
        command,
        result in wanted,
        f"expected {' or '.join(wanted)}, got {result}: {reasons}",
    )


def _validation_args(path: Path, root: Path, *, hosted: bool) -> list[str]:
    args = (
        ["tools/itws_comment.py", "validate", "--carrier"]
        if hosted
        else ["tools/itws_validate.py", "--input"]
    )
    args.append(path.relative_to(root).as_posix())
    return args


def check_fixtures(spec_dir: Path, root: Path) -> list[Step]:
    steps: list[Step] = []
    try:
        parse_specification(spec_dir)
    except SpecError as error:
        return [
            Step(
                "fixture suite",
                "python3 tools/itws_validate.py",
                False,
                str(error),
            )
        ]

    conforming = root / "tests" / "fixtures" / "documents" / "conforming"
    comments = root / "tests" / "fixtures" / "comments"
    for profile in PROFILE_IDS:
        hosted = PROFILE_SURFACES[profile] == "hosted-comment-set"
        path = (
            comments / "conforming" / "carrier.json"
            if hosted
            else conforming / f"{profile}.md"
        )
        if not path.exists():
            steps.append(
                Step(
                    f"fixture {profile}",
                    f"validate {profile}",
                    False,
                    "missing fixture",
                )
            )
            continue
        steps.append(
            run_validation(
                f"fixture {profile}",
                _validation_args(path, root, hosted=hosted),
                root,
                ("pass",),
            )
        )

    documents = root / "tests" / "fixtures" / "documents"
    for relative in (
        "violations/term-before-definition.md",
        "violations/procedure-reordered.md",
        "blocked/stale-version.md",
    ):
        path = documents / relative
        steps.append(
            run_validation(
                f"risk fixture {relative}",
                _validation_args(path, root, hosted=False),
                root,
                ("fail",),
            )
        )

    comment_expectations: dict[str, tuple[str, ...]] = {
        "conforming-removal": ("pass",),
        "violations/bare-marker": ("fail",),
        # A missing semantic basis is a candidate, not a workflow state.
        "violations/unsupported-rationale": ("pass",),
        # Proposal provenance and disposition belong to optional assurance.
        "violations/stale-proposal": ("pass",),
        "blocked/pending-disposition": ("pass",),
    }
    for relative, wanted in comment_expectations.items():
        path = comments / relative / "carrier.json"
        steps.append(
            run_validation(
                f"risk fixture comments/{relative}",
                _validation_args(path, root, hosted=True),
                root,
                wanted,
            )
        )
    return steps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="skip the unit-test step",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = REPO_ROOT
    spec_dir = (
        (root / args.spec_dir).resolve()
        if not args.spec_dir.is_absolute()
        else args.spec_dir
    )
    steps = [
        run_command(
            "overlay layout",
            ["tools/itws_overlays.py", "--spec-dir", str(args.spec_dir)],
            root,
        ),
        run_command(
            "navigation metadata",
            [
                "tools/itws_annotate.py",
                "--spec-dir",
                str(args.spec_dir),
                "--check",
            ],
            root,
        ),
        run_command(
            "Annex C",
            [
                "tools/itws_index.py",
                "--spec-dir",
                str(args.spec_dir),
                "--check",
            ],
            root,
        ),
        run_command(
            "generated catalog",
            [
                "tools/itws_compile.py",
                "--spec-dir",
                str(args.spec_dir),
                "--check",
            ],
            root,
        ),
    ]
    if not args.skip_tests:
        steps.append(
            run_command(
                "unit tests",
                [
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tests",
                    "-t",
                    ".",
                    "-q",
                ],
                root,
            )
        )
    steps.extend(check_fixtures(spec_dir, root))

    width = max(len(step.name) for step in steps)
    failures = 0
    for step in steps:
        mark = "ok  " if step.passed else "FAIL"
        print(f"{mark}  {step.name.ljust(width)}  {step.command}")
        if not step.passed:
            failures += 1
            for line in step.detail.splitlines():
                print(f"        {line}")
    print(f"\n{len(steps) - failures}/{len(steps)} step(s) passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
