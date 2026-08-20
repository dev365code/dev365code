#!/usr/bin/env python3
"""Render the profile: README.md and the two SVGs it points at.

    python render.py            # rebuild from the values below
    python render.py --live     # refresh what the API knows first
    python render.py --check    # fail if the committed files have drifted

Columns are computed here, never typed, so a value can change length without
anyone re-counting spaces. It is an SVG because a fenced code block cannot be
centred -- align=center resolves to text-align, which centres each line inside
the <pre> separately and tears the ASCII apart -- and because GitHub does not
render ANSI colour in Markdown.
"""
import json, os, pathlib, sys, urllib.request

HERE = pathlib.Path(__file__).parent
PANEL_W = 54
GAP = 5
FONT_PX, LINE_H, CW = 14, 20, 8.4
PAD = 26
ALIGN = os.environ.get("ALIGN", "left")     # left | stagger

HOST = "wooyong@lee"
ROWS = [
    ("row",  "OS",                    "macOS, Linux"),
    ("row",  "Shell",                 "zsh"),
    ("row",  "Editor",                "VS Code"),
    ("row",  "Location",              "Seoul, KR"),
    ("gap",),
    ("row",  "Languages.Programming", "Python, Java"),
    ("row",  "Languages.Data",        "SQL, RDF/SPARQL"),
    ("row",  "Languages.Real",        "Korean, English"),
    ("row",  "Hobbies",               "jigsaw puzzles"),
    ("sect", "Projects"),
    ("row",  "iirds-validate",        "185 rules, offline, Apache-2.0"),
    ("row",  "shannon-trading",       "volatility harvesting, live"),
    ("row",  "document AI",           "structure out of PDFs"),
    ("sect", "git status"),
    ("row",  "Latest push",           "iirds-validate, 2026-08-20"),
    ("sect", "Contact"),
    ("row",  "Email",                 "zero8004paz@gmail.com"),
    ("row",  "GitHub",                "dev365code"),
]

# dev / 365 / code, all figlet "colossal": 24, 30 and 32 columns wide, eight
# rows each. The widths climb, so left-aligning the three blocks lets the
# right edges step outward on their own -- no offset to hand-tune.
BLOCKS = [
    ("mark", r"""
     888
     888
     888
 .d88888 .d88b. 888  888
d88" 888d8P  Y8b888  888
888  88888888888Y88  88P
Y88b 888Y8b.     Y8bd8P
 "Y88888 "Y8888   Y88P"""),
    ("art", r"""
 .d8888b.  .d8888b. 888888888
d88P  Y88bd88P  Y88b888
     .d88P888       888
    8888" 888d888b. 8888888b.
     "Y8b.888P "Y88b     "Y88b
888    888888    888       888
Y88b  d88PY88b  d88PY88b  d88P
 "Y8888P"  "Y8888P"  "Y8888P" """),
    ("mark", r"""
                     888
                     888
                     888
 .d8888b .d88b.  .d88888 .d88b.
d88P"   d88""88bd88" 888d8P  Y8b
888     888  888888  88888888888
Y88b.   Y88..88PY88b 888Y8b.
 "Y8888P "Y88P"  "Y88888 "Y8888"""),
]

# Hermes orange is #F37021. On white it lands at 2.94:1, under WCAG AA, so the
# light theme keeps the hue and drops brightness to 75%, #BF581A (4.54:1).
THEMES = {
    "dark":  dict(art="#8b949e", mark="#F37021", label="#F37021",
                  value="#79c0ff", dim="#3d444d", host="#e6edf3"),
    "light": dict(art="#57606a", mark="#BF581A", label="#BF581A",
                  value="#0550AE", dim="#afb8c1", host="#1f2328"),
}

def api(url):
    tok = os.environ.get("GITHUB_TOKEN")
    hdr = {"Authorization": f"Bearer {tok}"} if tok else {}
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=hdr)))

def refresh():
    """Re-derive the rows the API knows better than a hand-edited file."""
    repos, page = [], 1
    while True:
        got = api(f"https://api.github.com/users/dev365code/repos"
                  f"?per_page=100&page={page}&sort=pushed")
        if not got:
            break
        repos += [r for r in got if not r["fork"]]
        page += 1
    tot = {}
    for r in repos:
        for k, v in api(r["languages_url"]).items():
            tot[k] = tot.get(k, 0) + v
    newest = max(repos, key=lambda r: r["pushed_at"])
    return {
        "Languages.Programming": ", ".join(sorted(tot, key=tot.get, reverse=True)[:2]),
        "Latest push": f'{newest["name"]}, {newest["pushed_at"][:10]}',
    }

def art_lines():
    blocks = [(role, [l for l in b.strip("\n").split("\n")]) for role, b in BLOCKS]
    w = max(len(l) for _, b in blocks for l in b)
    out = []
    for i, (role, b) in enumerate(blocks):
        bw = max(len(l) for l in b)
        pad = 0 if ALIGN == "left" else (0, (w - bw) // 2, w - bw)[i]
        out += [(role, " " * pad + l.rstrip()) for l in b]
    return out, w

def panel():
    lines = [[("host", HOST + " "), ("dim", "─" * (PANEL_W - len(HOST) - 1))]]
    for r in ROWS:
        if r[0] == "gap":
            lines.append([])
        elif r[0] == "sect":
            lines += [[], [("dim", "─ "), ("host", r[1] + " "),
                           ("dim", "─" * (PANEL_W - len(r[1]) - 3))]]
        else:
            label, value = r[1], r[2]
            dots = PANEL_W - 5 - len(label) - len(value)
            if dots < 3:
                raise SystemExit(f"PANEL_W={PANEL_W} too narrow: {label}")
            lines.append([("dim", ". "), ("label", f"{label}:"),
                          ("dim", " " + "." * dots + " "), ("value", value)])
    return lines

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def svg(theme):
    c = THEMES[theme]
    art, art_w = art_lines()
    rows_ = panel()
    n = max(len(art), len(rows_))
    w = round((art_w + GAP + PANEL_W) * CW) + PAD * 2
    h = n * LINE_H + PAD * 2
    px = PAD + (art_w + GAP) * CW
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}" font-family="ui-monospace,SFMono-Regular,'
           f'Menlo,Consolas,&quot;Liberation Mono&quot;,monospace" '
           f'font-size="{FONT_PX}">']

    def text(x, i, runs):
        chars = sum(len(t) for _, t in runs)
        if not chars:
            return
        # textLength pins the run to an exact width, so a monospace fallback
        # with a different advance ratio cannot push anything out of place.
        spans = "".join(f'<tspan fill="{c[k]}">{esc(t)}</tspan>' for k, t in runs)
        out.append(f'<text x="{x:.1f}" y="{PAD + i * LINE_H + FONT_PX}" '
                   f'xml:space="preserve" textLength="{chars * CW:.1f}" '
                   f'lengthAdjust="spacing">{spans}</text>')

    for i, (role, line) in enumerate(art):
        text(PAD, i + (n - len(art)) // 2, [(role, line)])
    for i, line in enumerate(rows_):
        text(px, i + (n - len(rows_)) // 2, line)
    out.append("</svg>")
    return "\n".join(out) + "\n"

README = """<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="profile-dark.svg">
    <img alt="{alt}" src="profile-light.svg" width="{w}">
  </picture>
</div>
"""

def build():
    files = {f"profile-{t}.svg": svg(t) for t in THEMES}
    alt = "dev365code - " + " / ".join(f"{r[1]}: {r[2]}" for r in ROWS if r[0] == "row")
    _, art_w = art_lines()
    files["README.md"] = README.format(
        alt=esc(alt), w=round((art_w + GAP + PANEL_W) * CW) + PAD * 2)
    return files

if "--live" in sys.argv:
    fresh = refresh()
    ROWS[:] = [(r[0], r[1], fresh.get(r[1], r[2])) if r[0] == "row" else r
               for r in ROWS]

files = build()
if "--check" in sys.argv:
    stale = [n for n, t in files.items() if (HERE / n).read_text() != t]
    sys.exit(f"stale, re-run render.py: {', '.join(stale)}" if stale else 0)
for n, t in files.items():
    (HERE / n).write_text(t)
    print(f"wrote {n}", file=sys.stderr)
