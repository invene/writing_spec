#!/usr/bin/env python3
"""Run every ITWS check in one command.

The command runs the overlay-layout check, specification parsing, Annex C
generation, artifact generation, the unit tests, the twelve-profile fixture
suite, and the risk fixtures. A conforming fixture is validated through the
path its profile surface requires: `itws_validate` for a Markdown document,
`itws_comment` for a hosted comment set.

Each step prints the equivalent single command, so a failure can be isolated
without rerunning the whole suite.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from itws.checklist import annex_revision, render
from itws.lint.model import Evidence
from itws.parser import SpecError, parse_specification
from itws.validate import validate_comment_set, validate_document
from itws.vocab import PROFILE_IDS, PROFILE_SURFACES


@dataclass
class Step:
    name: str
    command: str
    passed: bool
    detail: str = ""


def run_command(name: str, args: list[str], cwd: Path) -> Step:
    process = subprocess.run(
        [sys.executable, *args], cwd=cwd, capture_output=True, text=True
    )
    detail = (process.stdout + process.stderr).strip()
    return Step(
        name=name,
        command="python3 " + " ".join(args),
        passed=process.returncode == 0,
        detail="" if process.returncode == 0 else detail,
    )


def _full_evidence(spec, revision: str, checklist: Path | None) -> Evidence:
    return Evidence(
        checklist_path=checklist,
        checklist_annex_hash=revision,
        self_check_recorded=True,
        owner_review_recorded=True,
        proxy_review_recorded=True,
        reader_test_recorded=True,
        artifacts_current=True,
        lint_run_version=spec.version,
    )


def _validate_fixture(
    spec, spec_dir: Path, profile: str, path: Path, evidence: Evidence
):
    """Dispatch one conforming fixture by the profile's governed surface."""
    if PROFILE_SURFACES[profile] == "hosted-comment-set":
        return validate_comment_set(
            spec, path, spec_dir=spec_dir, evidence=evidence, check_artifacts=False
        )
    return validate_document(
        spec,
        path,
        spec_dir=spec_dir,
        evidence=evidence,
        network=True,
        check_artifacts=False,
    )


def check_fixtures(spec_dir: Path, root: Path) -> list[Step]:
    """Validate every profile fixture and the risk fixtures, by surface."""
    steps: list[Step] = []
    try:
        spec = parse_specification(spec_dir)
    except SpecError as error:
        return [Step("fixture suite", "python3 tools/itws_validate.py", False, str(error))]

    annex_c = spec_dir / "annexes" / "annex-c-rule-index.md"
    revision = annex_revision(annex_c.read_text(encoding="utf-8"), spec.version)

    conforming = root / "tests" / "fixtures" / "documents" / "conforming"
    for profile in PROFILE_IDS:
        if PROFILE_SURFACES[profile] == "hosted-comment-set":
            path = (
                root / "tests" / "fixtures" / "comments" / "conforming"
                / "carrier.json"
            )
            command = (
                "python3 tools/itws_comment.py validate --carrier "
                f"{path.relative_to(root)}"
            )
        else:
            path = conforming / f"{profile}.md"
            command = (
                f"python3 tools/itws_validate.py --input {path.relative_to(root)}"
            )
        if not path.exists():
            steps.append(Step(f"fixture {profile}", command, False, "missing fixture"))
            continue
        tier = spec.profile(profile).minimum_tier
        with tempfile.TemporaryDirectory() as raw:
            checklist = Path(raw) / "checklist.md"
            checklist.write_text(
                render(
                    spec,
                    profile=profile,
                    tier=tier,
                    generated_date="2026-07-29",
                    index_revision=revision,
                ),
                encoding="utf-8",
            )
            report = _validate_fixture(
                spec, spec_dir, profile, path,
                _full_evidence(spec, revision, checklist),
            )
        steps.append(
            Step(
                f"fixture {profile}",
                command,
                report.state == "pass",
                f"state {report.state}: " + "; ".join(report.reasons),
            )
        )

    expectations = {
        "violations/term-before-definition.md": "fail",
        "violations/procedure-reordered.md": "fail",
        "blocked/stale-version.md": ("fail", "blocked"),
    }
    documents = root / "tests" / "fixtures" / "documents"
    for relative, expected in expectations.items():
        path = documents / relative
        command = f"python3 tools/itws_validate.py --input {path.relative_to(root)}"
        report = validate_document(
            spec,
            path,
            spec_dir=spec_dir,
            evidence=_full_evidence(spec, revision, None),
            check_artifacts=False,
        )
        wanted = expected if isinstance(expected, tuple) else (expected,)
        steps.append(
            Step(
                f"risk fixture {relative}",
                command,
                report.state in wanted,
                f"expected {' or '.join(wanted)}, got {report.state}",
            )
        )

    comment_expectations = {
        "violations/bare-marker": "fail",
        "violations/unsupported-rationale": "fail",
        "violations/stale-proposal": "fail",
        "blocked/pending-disposition": "blocked",
    }
    comments = root / "tests" / "fixtures" / "comments"
    for relative, expected in comment_expectations.items():
        path = comments / relative / "carrier.json"
        command = (
            "python3 tools/itws_comment.py validate --carrier "
            f"{path.relative_to(root)}"
        )
        report = validate_comment_set(
            spec,
            path,
            spec_dir=spec_dir,
            evidence=_full_evidence(spec, revision, None),
            check_artifacts=False,
        )
        steps.append(
            Step(
                f"risk fixture comments/{relative}",
                command,
                report.state == expected,
                f"expected {expected}, got {report.state}",
            )
        )
    return steps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--skip-tests", action="store_true", help="skip the unit-test step"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = REPO_ROOT
    spec_dir = (root / args.spec_dir).resolve() if not args.spec_dir.is_absolute() else args.spec_dir

    steps: list[Step] = [
        run_command(
            "overlay layout",
            ["tools/itws_overlays.py", "--spec-dir", str(args.spec_dir)],
            root,
        ),
        run_command(
            "navigation metadata",
            ["tools/itws_annotate.py", "--spec-dir", str(args.spec_dir), "--check"],
            root,
        ),
        run_command(
            "Annex C",
            ["tools/itws_index.py", "--spec-dir", str(args.spec_dir), "--check"],
            root,
        ),
        run_command(
            "generated catalog",
            ["tools/itws_compile.py", "--spec-dir", str(args.spec_dir), "--check"],
            root,
        ),
    ]
    if not args.skip_tests:
        steps.append(
            run_command(
                "unit tests",
                ["-m", "unittest", "discover", "-s", "tests", "-t", ".", "-q"],
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
    if failures:
        print("Rerun the failing command above to isolate the defect.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
