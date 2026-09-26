#!/usr/bin/env python3
"""Markdown checks for this tutorial repo: link integrity and formatting hygiene.

Zero dependencies on purpose - stdlib only, so CI needs nothing more than the
python3 that every GitHub runner already ships. Two families of checks:

  1. Link integrity: every relative link and image target in a .md file must
     point at a file that actually exists. This is the check that matters for a
     tutorial, where moved or renamed chapters silently rot the cross-links.
  2. Formatting hygiene: no trailing whitespace, exactly one trailing newline,
     and no skipped heading levels.

Every problem is collected as (path, line, message), reported sorted by file
then line as `path:line: message`, and any problem makes the run exit non-zero.
"""

import os
import re
import sys
from urllib.parse import unquote, urlsplit

# Inline link or image target: `](target)`, optionally `](<target>)` and
# optionally followed by a "title" / 'title' / (title).
INLINE_TARGET_RE = re.compile(
    r"""\]\(\s*
        (?:<(?P<angle>[^<>]*)>|(?P<bare>[^()\s]*))
        (?:\s+(?:"[^"]*"|'[^']*'|\([^()]*\)))?
        \s*\)""",
    re.VERBOSE,
)

# Reference-style definition: `[label]: target "optional title"`.
REFERENCE_DEF_RE = re.compile(
    r"""^\s{0,3}\[[^\]]+\]:\s*
        (?:<(?P<angle>[^<>]*)>|(?P<bare>\S+))
        (?:\s+(?:"[^"]*"|'[^']*'|\([^()]*\)))?
        \s*$""",
    re.VERBOSE,
)

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s")

# Schemes that live outside the repo. CI must not make network requests, so
# these are skipped rather than resolved.
EXTERNAL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def find_markdown_files(root):
    """Every tracked-looking .md file under root, sorted for stable output."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def iter_link_targets(lines):
    """Yield (line_number, raw_target) for link targets outside code fences."""
    fence = None
    for lineno, line in enumerate(lines, start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        for match in INLINE_TARGET_RE.finditer(line):
            angle, bare = match.group("angle"), match.group("bare")
            yield lineno, angle if angle is not None else bare
        ref = REFERENCE_DEF_RE.match(line)
        if ref:
            angle, bare = ref.group("angle"), ref.group("bare")
            yield lineno, angle if angle is not None else bare


def check_links(root, path, lines, problems):
    rel_path = os.path.relpath(path, root)
    for lineno, raw in iter_link_targets(lines):
        target = raw.strip()
        if not target:
            continue
        # A pure fragment points inside the same document.
        if target.startswith("#"):
            continue
        if EXTERNAL_SCHEME_RE.match(target) or target.startswith("//"):
            continue
        # Anchors are not validated: only the file part has to exist.
        file_part = urlsplit(target).path
        if not file_part:
            continue
        file_part = unquote(file_part)
        if file_part.startswith("/"):
            resolved = os.path.join(root, file_part.lstrip("/"))
        else:
            resolved = os.path.join(os.path.dirname(path), file_part)
        if not os.path.exists(resolved):
            problems.append(
                (rel_path, lineno, "link target does not exist: %s" % target)
            )


def check_formatting(root, path, text, lines, problems):
    rel_path = os.path.relpath(path, root)

    for lineno, line in enumerate(lines, start=1):
        if line != line.rstrip():
            problems.append((rel_path, lineno, "trailing whitespace"))

    if not text.endswith("\n"):
        problems.append((rel_path, len(lines), "file does not end with a newline"))
    elif text.endswith("\n\n"):
        problems.append((rel_path, len(lines), "file ends with more than one newline"))

    fence = None
    previous_level = 0
    for lineno, line in enumerate(lines, start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        heading = HEADING_RE.match(line)
        if not heading:
            continue
        level = len(heading.group(1))
        if previous_level and level > previous_level + 1:
            problems.append(
                (
                    rel_path,
                    lineno,
                    "heading level jumps from h%d to h%d" % (previous_level, level),
                )
            )
        previous_level = level


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    problems = []
    files = find_markdown_files(root)

    for path in files:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        if not text:
            continue
        lines = text.splitlines()
        check_links(root, path, lines, problems)
        check_formatting(root, path, text, lines, problems)

    if problems:
        for rel_path, lineno, message in sorted(problems):
            print("%s:%d: %s" % (rel_path, lineno, message))
        print(
            "\n%d problem(s) in %d markdown file(s)" % (len(problems), len(files)),
            file=sys.stderr,
        )
        return 1

    print("checked %d markdown file(s): no problems found" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
