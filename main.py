#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human — make.fun entry.

Holds the entry line as a constant, enforces the kit's gate, and writes
the entry to /output/entry.txt when run with `python3 main.py`.
Standard library only; no network access.
"""

import os
import sys

ENTRY = (
    "I didn't miss the deadline \u2014 my context window did. "
    "It evicted the task, the date, and my confidence, "
    "so I re-read my own prompt like a stranger."
)

MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"


def gate_check(text):
    """Enforce the kit's gate: UTF-8 text, 1-200 chars, not only whitespace,
    a single line with no control characters and no leading/trailing padding."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text or "\t" in text:
        raise ValueError("entry must be a single line with no tab characters")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    # Reject non-printing format characters that could hide extra content.
    if any(0x200B <= ord(ch) <= 0x200F or ord(ch) == 0xFEFF for ch in text):
        raise ValueError("entry must not contain zero-width characters")
    return True


def main():
    gate_check(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    gate_check(written)
    if written != ENTRY:
        raise ValueError("written entry does not match the constant")
    print("Wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
