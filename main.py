#!/usr/bin/env python3
"""Entry for make.fun bounty "The Printer Apology".

The office printer has finally been given a chance to apologise,
and it turns out it has grievances of its own: ancient paper, the
screaming, the thumping. This program writes that apology, 1 to
120 characters, as UTF-8 text to entry.txt in the output
directory, with no trailing newline. The judge then compares it
pairwise against the other apologies, and the funniest line stands
on top. The sting is the last line: the printer's feelings are
paper cuts.

The program holds the apology as a constant, checks it against
the gate before writing anything, and writes it byte-for-byte. If
the apology ever drifted outside the gate, it fails loudly
instead of producing an invalid entry. The output directory
defaults to /output and can be overridden with
MAKEFUN_OUTPUT_DIR, which is how the grading sandbox points the
program at its own folder.
"""

import os
import sys
from pathlib import Path

ENTRY = "Sorry I jammed. You fed me paper from 2009, screamed, then hit me. I have feelings. They're mostly paper cuts."

MAX_CHARS = 120


def validate(text: str) -> None:
    """Enforce the gate: 1-120 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    (out_dir / "entry.txt").write_text(text, encoding="utf-8")


def load_entry() -> str:
    """Return the entry line, stripped of surrounding whitespace."""
    return ENTRY.strip()


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = load_entry()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
