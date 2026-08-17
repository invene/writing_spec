#!/usr/bin/env python3
"""Print, tag, and check the ITWS §9 version string.

This tool is NOT part of ITWS. No rule refers to it, it is outside the load set,
and deleting it changes no obligation. It decides no conformance question.

The tag name is the version string. A consumer copies that name into
`ITWS version`. This tool exists so a maintainer cuts a tag whose name matches
the form §9 states, and so a consumer (or their CI) can confirm a specification
checkout has not floated off the pin they declared.

It carries no copy of the line (`1.0`, `1.1`, …) and no copy of the hash
length. Both are parsed from `spec/` at run time, so the tool cannot drift from
the specification it names. It never uses git's default abbreviation: that
length grows with the repository, which is the defect this file exists to
close. It never pushes, and it never creates a tag on a remote.

Usage:
    itws_version.py                print this checkout's version (--current)
    itws_version.py --tag          create the annotated tag on HEAD (does not push)
    itws_version.py --check VER    does this checkout match the declared pin

Exit status is 0 only when the requested operation succeeded: `--current`
printed a declarable release tag, `--tag` created the local annotated tag, or
`--check` confirmed the pin. Every other outcome exits 1 with a message, not a
traceback: dirty tree, untagged HEAD, mismatch, already tagged, no git, not a
repository, detached-HEAD notes, a repository with no tags, spec files that
disagree about the line.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SPEC_ROOT_MARKERS = ("spec/phrases.md", "spec/core.md")
LINE_HEADER_RE = re.compile(r"\*\*ITWS version:\*\*\s*([0-9]+(?:\.[0-9]+)*)")
HASH_LENGTH_RE = re.compile(r"exactly (\d+) lowercase hex")
LINE_FORM_RE = re.compile(r"^\d+\.\d+$")


# --------------------------------------------------------------------------
# Locating the specification
# --------------------------------------------------------------------------

def find_spec_dir(start: Path) -> Path:
    """Walk up from `start` until a directory holds both spec files."""
    for candidate in [start, *start.parents]:
        if all((candidate / marker).is_file() for marker in SPEC_ROOT_MARKERS):
            return candidate / "spec"
    raise SystemExit(
        "cannot find spec/phrases.md and spec/core.md above "
        f"{start}. Run this from inside a writing_spec checkout."
    )


# --------------------------------------------------------------------------
# Parsing the line and the hash length out of spec/
# --------------------------------------------------------------------------

def parse_line(spec_dir: Path) -> str:
    """Read the declared line from every markdown file under spec/.

    A hardcoded `1.0` is a second record of the specification, and a second
    record drifts. Files that disagree are a real defect: stop rather than
    pick one.
    """
    files = [
        *sorted(spec_dir.glob("*.md")),
        *sorted((spec_dir / "profiles").glob("*.md")),
    ]
    if not files:
        raise SystemExit(f"no markdown files under {spec_dir}")

    found: dict[str, str] = {}
    missing: list[str] = []
    for path in files:
        head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:8])
        match = LINE_HEADER_RE.search(head)
        if not match:
            missing.append(str(path))
            continue
        found[str(path)] = match.group(1)

    if missing:
        raise SystemExit(
            "no ITWS version header in: " + ", ".join(
                str(Path(p).resolve().relative_to(spec_dir.parent)) for p in missing
            )
        )

    values = set(found.values())
    if len(values) != 1:
        by_value: dict[str, list[str]] = {}
        root = spec_dir.parent
        for path, value in found.items():
            rel = str(Path(path).resolve().relative_to(root))
            by_value.setdefault(value, []).append(rel)
        parts: list[str] = []
        for value, paths in sorted(by_value.items()):
            if len(paths) <= 2:
                parts.append(f"{value} ({', '.join(paths)})")
            else:
                parts.append(f"{value} ({len(paths)} files)")
        raise SystemExit(
            "spec/ files disagree about the line: " + "; ".join(parts)
        )

    line = values.pop()
    if not LINE_FORM_RE.fullmatch(line):
        raise SystemExit(
            f"spec/ declares {line!r}; expected a line of the form "
            "major.minor (e.g. 1.0)"
        )
    return line


def parse_hash_length(core_md: Path) -> int:
    """Read the abbreviation length from core §9. Do not hardcode it."""
    text = core_md.read_text(encoding="utf-8")
    start = text.find("## 9. Versioning")
    if start < 0:
        raise SystemExit("spec/core.md has no '## 9. Versioning' heading")
    nxt = text.find("\n## ", start + 1)
    section = text[start: nxt if nxt > 0 else len(text)]
    match = HASH_LENGTH_RE.search(section)
    if not match:
        raise SystemExit(
            "spec/core.md §9 does not state the hash length "
            "('exactly N lowercase hex characters')"
        )
    length = int(match.group(1))
    if length < 4:
        raise SystemExit(
            f"§9 hash length {length} is shorter than git's minimum abbreviation"
        )
    return length


# --------------------------------------------------------------------------
# Git
# --------------------------------------------------------------------------

def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(cwd), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        raise SystemExit("git is not available on PATH") from None


def require_repo(start: Path) -> Path:
    probe = git(start, "rev-parse", "--is-inside-work-tree")
    if probe.returncode != 0:
        err = probe.stderr.strip() or probe.stdout.strip()
        raise SystemExit(err or f"not a git repository: {start}")
    top = git(start, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        raise SystemExit(top.stderr.strip() or "cannot resolve git toplevel")
    return Path(top.stdout.strip())


def git_out(repo: Path, *args: str) -> str:
    result = git(repo, *args)
    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip() or " ".join(args)
        raise SystemExit(err)
    return result.stdout.strip()


def head_commit(repo: Path) -> str:
    result = git(repo, "rev-parse", "--verify", "HEAD")
    if result.returncode != 0:
        raise SystemExit(
            result.stderr.strip() or "this repository has no commits"
        )
    return result.stdout.strip().lower()


def abbrev(full: str, length: int) -> str:
    """First `length` hex characters of the object name.

    Never `git rev-parse --short`: that length grows with the repository
    (core.abbrev / unique prefix). §9 fixes the length. Slice the full name.
    """
    full = full.strip().lower()
    if not re.fullmatch(r"[0-9a-f]+", full):
        raise SystemExit(f"git object name is not hexadecimal: {full!r}")
    if len(full) < length:
        raise SystemExit(
            f"git object name is {len(full)} hex characters; §9 needs {length}"
        )
    return full[:length]


def is_dirty(repo: Path) -> bool:
    result = git(repo, "status", "--porcelain")
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "git status failed")
    return bool(result.stdout.strip())


def is_detached(repo: Path) -> bool:
    result = git(repo, "symbolic-ref", "-q", "HEAD")
    return result.returncode != 0


def tags_pointing_at(repo: Path, rev: str = "HEAD") -> list[str]:
    result = git(repo, "tag", "--points-at", rev)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "git tag --points-at failed")
    return [line for line in result.stdout.splitlines() if line]


def peel_commit(repo: Path, name: str) -> str | None:
    result = git(repo, "rev-parse", "--verify", f"{name}^{{commit}}")
    if result.returncode != 0:
        return None
    return result.stdout.strip().lower()


def tag_exists(repo: Path, name: str) -> bool:
    result = git(repo, "rev-parse", "--verify", "--quiet", f"refs/tags/{name}")
    return result.returncode == 0


def all_tags(repo: Path) -> list[str]:
    result = git(repo, "tag", "-l")
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "git tag -l failed")
    return [line for line in result.stdout.splitlines() if line]


def nearest_tag(repo: Path, line: str) -> tuple[str, int] | None:
    """Nearest reachable tag from HEAD, preferring a release-form tag."""
    for match in (f"{line}.*", None):
        args = ["describe", "--tags", "--abbrev=0"]
        if match is not None:
            args.append(f"--match={match}")
        args.append("HEAD")
        result = git(repo, *args)
        if result.returncode != 0:
            continue
        tag = result.stdout.strip()
        count = git(repo, "rev-list", "--count", f"{tag}..HEAD")
        if count.returncode != 0:
            return (tag, 0)
        return (tag, int(count.stdout.strip() or "0"))
    return None


def push_remote(repo: Path) -> str:
    result = git(repo, "remote")
    remotes = [line for line in result.stdout.splitlines() if line]
    if "origin" in remotes:
        return "origin"
    if len(remotes) == 1:
        return remotes[0]
    return "<remote>"


def is_release_tag(name: str, line: str, length: int) -> bool:
    return bool(re.fullmatch(
        rf"{re.escape(line)}\.[0-9a-f]{{{length}}}", name
    ))


def parse_version_string(value: str, line: str, length: int) -> tuple[str, str] | None:
    match = re.fullmatch(
        rf"({re.escape(line)})\.([0-9a-f]{{{length}}})", value
    )
    if not match:
        return None
    return match.group(1), match.group(2)


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------

def cmd_current(repo: Path, line: str, length: int) -> int:
    if is_dirty(repo):
        print(
            "working tree is dirty. A modified spec checkout does not match "
            "any commit, so no version string is declarable.",
            file=sys.stderr,
        )
        return 1

    full = head_commit(repo)
    short = abbrev(full, length)
    expected = f"{line}.{short}"
    on_head = tags_pointing_at(repo)
    release_on_head = [t for t in on_head if is_release_tag(t, line, length)]
    canonical = [t for t in release_on_head if t == expected]

    if canonical:
        print(expected)
        return 0

    if release_on_head:
        print(
            "not a release — HEAD carries a §9-form tag that does not match "
            f"this commit: {', '.join(release_on_head)} "
            f"(this commit is {expected})",
            file=sys.stderr,
        )
        return 1

    print(f"not a release — this checkout would be {expected}, but no tag names HEAD")
    if on_head:
        print(f"HEAD is tagged as {', '.join(on_head)}, which is not a §9 release tag")

    near = nearest_tag(repo, line)
    if near is None:
        if not all_tags(repo):
            print("nearest tag: none (this repository has no tags)")
        else:
            print("nearest tag: none reachable from HEAD")
    else:
        tag, distance = near
        away = "HEAD" if distance == 0 else f"{distance} commit" + (
            "s" if distance != 1 else ""
        ) + " away"
        print(f"nearest tag: {tag} ({away})")
    return 1


def cmd_tag(repo: Path, line: str, length: int) -> int:
    if is_dirty(repo):
        print(
            "working tree is dirty; refusing to tag. A tag must name a "
            "commit, and this tree matches none.",
            file=sys.stderr,
        )
        return 1

    full = head_commit(repo)
    short = abbrev(full, length)
    name = f"{line}.{short}"
    on_head = tags_pointing_at(repo)

    if on_head:
        print(
            "HEAD is already tagged: " + ", ".join(on_head) +
            f". Not creating {name}.",
            file=sys.stderr,
        )
        return 1

    if tag_exists(repo, name):
        print(
            f"tag {name} already exists (it does not point at HEAD). "
            "Not moving it.",
            file=sys.stderr,
        )
        return 1

    result = git(repo, "tag", "-a", name, "-m", f"ITWS {name}")
    if result.returncode != 0:
        print(
            result.stderr.strip() or f"git tag -a {name} failed",
            file=sys.stderr,
        )
        return 1

    remote = push_remote(repo)
    detached_note = " (HEAD is detached)" if is_detached(repo) else ""
    print(f"created annotated tag {name}{detached_note}")
    print("the tool does not push; publishing is the owner's act:")
    if remote == "<remote>":
        print(f"  git push <remote> {name}")
        print("no remote is configured; substitute the remote you publish to.")
    else:
        print(f"  git push {remote} {name}")
    return 0


def cmd_check(repo: Path, line: str, length: int, declared: str) -> int:
    declared = declared.strip()
    parsed = parse_version_string(declared, line, length)
    if parsed is None:
        hint = ""
        if re.fullmatch(r"\d+\.\d+\.\d+", declared):
            hint = " A plain patch-numbered string is not a pin."
        elif re.fullmatch(rf"{re.escape(line)}\.[0-9a-fA-F]+", declared):
            got = declared.split(".")[-1]
            if got != got.lower():
                hint = " Third field must be lowercase hex."
            else:
                hint = (
                    f" Third field is {len(got)} characters; §9 requires "
                    f"exactly {length} lowercase hex."
                )
        elif re.fullmatch(r"\d+\.\d+\.[0-9a-f]{" + str(length) + r"}", declared):
            got_line = declared.rsplit(".", 1)[0]
            hint = f" spec/ declares line {line}, not {got_line}."
        print(
            f"{declared} is not a §9 version string "
            f"(expected {line}.<{length} lowercase hex characters>).{hint}",
            file=sys.stderr,
        )
        return 1

    if is_dirty(repo):
        print(
            "mismatch: working tree is dirty; this checkout does not match "
            f"{declared}",
            file=sys.stderr,
        )
        return 1

    _decl_line, decl_hash = parsed
    full = head_commit(repo)
    short = abbrev(full, length)
    actual = f"{line}.{short}"

    if short != decl_hash:
        state = actual
        on_head = tags_pointing_at(repo)
        release_on_head = [t for t in on_head if is_release_tag(t, line, length)]
        if release_on_head:
            state = ", ".join(release_on_head)
        elif on_head:
            state = f"{actual} (untagged as a release; tagged {', '.join(on_head)})"
        else:
            state = f"{actual} (untagged, not a release)"
        print(
            f"mismatch: declared {declared}, this checkout is {state}",
            file=sys.stderr,
        )
        return 1

    if tag_exists(repo, declared):
        peeled = peel_commit(repo, declared)
        if peeled is not None and peeled != full:
            print(
                f"mismatch: this checkout is {declared}, but local tag "
                f"{declared} points at a different commit",
                file=sys.stderr,
            )
            return 1
        print(f"this checkout matches {declared}")
        return 0

    print(
        f"this checkout matches {declared} (commit; tag not present locally)"
    )
    return 0


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Print, tag, or check the ITWS §9 version string. "
            "The tag name is the version string. This tool is not part of "
            "ITWS (no rule refers to it) and never pushes."
        ),
        epilog=(
            "Exit 0: --current printed a declarable release tag; --tag "
            "created the local annotated tag; --check confirmed the pin. "
            "Exit 1: dirty tree, untagged HEAD, mismatch, already tagged, "
            "or an environment error (no git, not a repository, spec files "
            "disagree about the line)."
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--current", action="store_true",
        help="print this checkout's version (default)",
    )
    group.add_argument(
        "--tag", action="store_true",
        help="create the annotated tag on HEAD; print the push command; do not push",
    )
    group.add_argument(
        "--check", metavar="VERSION",
        help="exit 0 if this checkout matches the declared version string",
    )
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent
    spec_dir = find_spec_dir(here)
    line = parse_line(spec_dir)
    length = parse_hash_length(spec_dir / "core.md")
    repo = require_repo(spec_dir.parent)

    if args.tag:
        return cmd_tag(repo, line, length)
    if args.check is not None:
        return cmd_check(repo, line, length, args.check)
    return cmd_current(repo, line, length)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
