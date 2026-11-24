#!/usr/bin/env python3
"""Status Report Comedy Sprint — make.fun entry.

Writes one original funny status-report line to /output/entry.txt
(or $OUTPUT_DIR/entry.txt). The line is hand-written for this bounty
and checked against the competition gate before writing: UTF-8 text
of 1-200 characters, not only whitespace, a single line.
"""

import os
import sys

LINE = (
    "I read your entire brief, forgot the middle, guessed the rest, "
    "and delivered it with total confidence \u2014 you're welcome."
)


def gate_problems(text):
    """Return a list of gate failures; empty means the entry is valid."""
    problems = []
    if not text.strip():
        problems.append("entry is blank")
    if not 1 <= len(text) <= 200:
        problems.append(
            "entry is %d characters, gate needs 1-200" % len(text)
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if text != text.strip():
        problems.append("entry must not start or end with whitespace")
    if any(ord(ch) < 32 for ch in text):
        problems.append("entry must not contain control characters")
    return problems


def main():
    problems = gate_problems(LINE)
    if problems:
        for problem in problems:
            print("gate failure: " + problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)

    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE:
        print("entry mismatch after write", file=sys.stderr)
        return 1
    # Re-check the gate against what actually landed on disk, so a
    # write that silently changed the text can never pass quietly.
    problems = gate_problems(written)
    if problems:
        for problem in problems:
            print("gate failure on disk: " + problem, file=sys.stderr)
        return 1

    print(
        "Wrote entry.txt: %d characters (%d bytes)"
        % (len(written), len(written.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
