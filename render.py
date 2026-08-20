#!/usr/bin/env python3
"""Render README.md.  python render.py > README.md

Columns are computed, not typed, so a value can change length without
anyone re-counting spaces. --check fails when README.md has drifted.
"""
import sys, pathlib

W = 56          # panel width; matches the banner
RULE = "\u2500"  # box drawing light horizontal

BANNER = r"""
       __         _____ _____ ______               __
  ____/ /__ _   _|__  // ___// ____/________  ____/ /__
 / __  / _ \ | / //_ </ __ \/___ \/ ___/ __ \/ __  / _ \
/ /_/ /  __/ |/ /__/ / /_/ /___/ / /__/ /_/ / /_/ /  __/
\__,_/\___/|___/____/\____/_____/\___/\____/\__,_/\___/
""".strip("\n")

HOST = "wylee@github"
ROWS = [
    ("OS",    "macOS, Linux"),
    ("Shell", "zsh"),
    ("Lang",  "Python, Java"),
    ("Work",  "document AI, trading, backend"),
    ("OSS",   "iirds-validate \u00b7 185 rules, offline"),
    ("Email", "zero8004paz@gmail.com"),
]

def row(label, value):
    dots = W - 5 - len(label) - len(value)
    if dots < 3:
        raise SystemExit(f"W={W} too narrow for row: {label}")
    return f'. {label}: {"." * dots} {value}'

out = ["```text", BANNER, "", f'{HOST} {RULE * (W - len(HOST) - 1)}']
out += [row(*r) for r in ROWS]
out.append("```")
text = "\n".join(out) + "\n"

if "--check" in sys.argv:
    have = pathlib.Path(__file__).with_name("README.md").read_text()
    sys.exit(0 if have == text else "README.md is stale \u2014 re-run render.py")
sys.stdout.write(text)
