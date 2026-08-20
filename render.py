#!/usr/bin/env python3
"""Render README.md for this profile.

    python render.py > README.md          # colour, via ANSI in an ```ansi fence
    python render.py --plain > README.md  # monochrome fallback

Every column is computed here, never typed by hand, so a value can change
length without anyone re-counting spaces. `--check` re-renders and diffs
against README.md, so a stale README fails instead of drifting quietly.
"""
import sys, pathlib

W = 64                                        # panel width, in columns
PLAIN = "--plain" in sys.argv

C = {"dim": "\033[90m", "label": "\033[33m", "value": "\033[34m",
     "head": "\033[1m", "off": "\033[0m"}
if PLAIN:
    C = dict.fromkeys(C, "")

BANNER = r"""
       __         _____ _____ ______               __
  ____/ /__ _   _|__  // ___// ____/________  ____/ /__
 / __  / _ \ | / //_ </ __ \/___ \/ ___/ __ \/ __  / _ \
/ /_/ /  __/ |/ /__/ / /_/ /___/ / /__/ /_/ / /_/ /  __/
\__,_/\___/|___/____/\____/_____/\___/\____/\__,_/\___/
""".strip("\n")
PAD = (W - max(len(l) for l in BANNER.split("\n"))) // 2

ROWS = [
    ("head", "wylee@github"),
    ("row",  "OS",                    "macOS, Linux"),
    ("row",  "Shell",                 "zsh"),
    ("row",  "Editor",                "VS Code"),
    ("row",  "Location",              "Seoul, KR"),
    ("gap",),
    ("row",  "Languages.Programming", "Python, Java, JavaScript"),
    ("row",  "Languages.Data",        "SQL, RDF/SPARQL"),
    ("row",  "Languages.Real",        "Korean, English"),
    ("gap",),
    ("row",  "Hobbies.Software",      "algorithmic trading, ASCII art"),
    ("row",  "Hobbies.Hardware",      "embedded Linux"),
    ("sect", "Projects"),
    ("row",  "iirds-validate",        "185 rules, offline, Apache-2.0"),
    ("row",  "shannon-trading",       "volatility harvesting, live"),
    ("row",  "document AI",           "structure out of PDFs"),
    ("sect", "Contact"),
    ("row",  "Email",                 "zero8004paz@gmail.com"),
    ("row",  "GitHub",                "dev365code"),
]

def row(label, value):
    dots = W - 5 - len(label) - len(value)
    if dots < 3:
        raise SystemExit(f"W={W} too narrow for row: {label}")
    return (f'{C["dim"]}. {C["label"]}{label}:{C["dim"]} {"." * dots} '
            f'{C["value"]}{value}{C["off"]}')

def head(t): return f'{C["head"]}{t} {C["dim"]}{"─" * (W - len(t) - 1)}{C["off"]}'
def sect(t): return f'{C["dim"]}─ {C["head"]}{t} {C["dim"]}{"─" * (W - len(t) - 3)}{C["off"]}'

out = ["```text" if PLAIN else "```ansi"]
out += [" " * PAD + l for l in BANNER.split("\n")] + [""]
for r in ROWS:
    if r[0] == "sect": out.append("")
    out.append({"head": lambda: head(r[1]), "sect": lambda: sect(r[1]),
                "gap": lambda: "", "row": lambda: row(r[1], r[2])}[r[0]]())
out.append("```")
text = "\n".join(out) + "\n"

if "--check" in sys.argv:
    have = pathlib.Path(__file__).with_name("README.md").read_text()
    sys.exit(0 if have == text else "README.md is stale — re-run render.py")
sys.stdout.write(text)
