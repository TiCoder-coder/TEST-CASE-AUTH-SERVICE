#!/usr/bin/env python3
import os
from _paths import EVIDENCE_DIR_C09, EVIDENCE_DIR_C10

"""Pretty-print JSON inside markdown code blocks for evidence files.

Finds ```json\n(RAW)\n``` blocks where RAW is valid JSON, replaces with pretty-printed
version with 2-space indent. Preserves all other markdown content."""
import re
import json
import sys
import glob

EVIDENCE_GLOB = os.path.join(EVIDENCE_DIR_C10, "**", "*.md")


def pretty(s):
    """Pretty-print JSON with 2-space indent."""
    parsed = json.loads(s)
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def is_simple_enough(s):
    """Return True if string is JSON and can be pretty-printed."""
    try:
        json.loads(s)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def format_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks_formatted = 0

    # Match ```json\n(RAW)\n``` - RAW is anything until closing ```
    # Using re.sub with callback
    pattern = re.compile(r"```json\n(.*?)\n```", re.DOTALL)

    def repl(m):
        nonlocal blocks_formatted
        raw = m.group(1)
        if not is_simple_enough(raw):
            return m.group(0)
        try:
            new = pretty(raw)
            if new != raw:
                blocks_formatted += 1
                return f"```json\n{new}\n```"
        except Exception:
            pass
        return m.group(0)

    new_content = pattern.sub(repl, content)

    if blocks_formatted > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

    return blocks_formatted


def main():
    total = 0
    files = glob.glob(EVIDENCE_GLOB, recursive=True)
    for path in files:
        n = format_file(path)
        if n > 0:
            print(f"  {path.split('/')[-1]}: {n} blocks formatted")
            total += n
    print(f"\nTotal: {total} JSON code blocks formatted")
    return 0


if __name__ == "__main__":
    sys.exit(main())