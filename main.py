#!/usr/bin/env python3
"""The Internet in One Word — one-word entry for make.fun.

The entry is a single deterministic word: no randomness, no network, no
clock. It is printed to stdout and written verbatim to the entry file.
"""

import os
from pathlib import Path

MAX_LENGTH = 30

WORD = 'Enshittification'


def _fail(message: str) -> None:
    raise SystemExit(message)


def _checks(word: str):
    """Yield (passed, message) for every rule the word must satisfy."""
    yield bool(word.strip()), "Invalid word: entry must be non-empty."
    yield word == word.strip(), (
        "Invalid word: entry must not have leading or trailing whitespace."
    )
    yield len(word) <= MAX_LENGTH, (
        f"Invalid word: {len(word)} characters, over the {MAX_LENGTH} limit."
    )
    yield " " not in word and "\n" not in word and "\r" not in word, (
        "Invalid word: entry must be a single word with no spaces or newlines."
    )
    yield word.isalpha(), "Invalid word: entry must be a single word."


def validate(word: str) -> None:
    for passed, message in _checks(word):
        if not passed:
            _fail(message)


def _output_path() -> Path:
    return Path(os.environ.get("OUTPUT_PATH", "/output/entry.txt"))


def _write_entry(path: Path, word: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(word, encoding="utf-8")
    if path.read_text(encoding="utf-8") != word:
        _fail(
            "Write verification failed: entry file content does not match the word."
        )


def main() -> int:
    validate(WORD)
    _write_entry(_output_path(), WORD)
    print(WORD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
