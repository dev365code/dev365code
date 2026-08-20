#!/usr/bin/env python3
"""Render the profile: README.md and the two SVGs it points at.

    python render.py            # rebuild from the values below
    python render.py --live     # refresh Lang from the GitHub API first
    python render.py --check    # fail if the committed files have drifted

Columns are computed here, never typed, so a value can change length
without anyone re-counting spaces. The SVG exists because a fenced code
block cannot be centred without text-align breaking the ASCII, and because
GitHub does not render ANSI colour in Markdown.
"""
import json, os, pathlib, sys, urllib.request

HERE = pathlib.Path(__file__).parent
PANEL_W = 52
GAP = 4
FONT_PX, LINE_H, CW = 14, 20, 8.4
PAD = 24

HOST = "wooyong@lee"
DATA = [
    ("OS",    "macOS, Linux"),
    ("Shell", "zsh"),
    ("Lang",  "Python, Java"),
    ("Work",  "document AI, trading, backend"),
    ("Hobby", "jigsaw puzzles"),
    ("OSS",   "iirds-validate · 185 rules, offline"),
    ("Email", "zero8004paz@gmail.com"),
]

ART = r"""
 .d8888b.  .d8888b. 888888888
d88P  Y88bd88P  Y88b888
     .d88P888       888
    8888" 888d888b. 8888888b.
     "Y8b.888P "Y88b     "Y88b
888    888888    888       888
Y88b  d88PY88b  d88PY88b  d88P
 "Y8888P"  "Y8888P"  "Y8888P"
""".strip("\n").split("\n")

# Hermes orange is #F37021. On white it lands at 2.94:1, under WCAG AA, so
# the light theme keeps the hue and drops the brightness to 75% (4.54:1).
THEMES = {
    "dark":  dict(art="#8b949e", label="#F37021", value="#79c0ff",
                  dim="#3d444d", host="#e6edf3"),
    "light": dict(art="#57606a", label="#BF581A", value="#0550AE",
                  dim="#afb8c1", host="#1f2328"),
}

def lang_from_api():
    """Bytes per language across every non-fork repo, most-used first."""
    tok = os.environ.get("GITHUB_TOKEN")
    hdr = {"Authorization": f"Bearer {tok}"} if tok else {}
    get = lambda u: json.load(urllib.request.urlopen(
        urllib.request.Request(u, headers=hdr)))
    tot, page = {}, 1
    while True:
        url = f"https://api.github.com/users/dev365code/repos?per_page=100&page={page}"
        repos = get(url)
        if not repos:
            break
        for r in repos:
            if r["fork"]:
                continue
            for k, v in get(r["languages_url"]).items():
                tot[k] = tot.get(k, 0) + v
        page += 1
    top = sorted(tot, key=tot.get, reverse=True)[:2]
    return ", ".join(top)

def rows():
    """(label, value) -> the three coloured runs that make up one line."""
    for label, value in DATA:
        dots = PANEL_W - 5 - len(label) - len(value)
        if dots < 3:
            raise SystemExit(f"PANEL_W={PANEL_W} too narrow for row: {label}")
        yield [("dim", ". "), ("label", f"{label}:"),
               ("dim", " " + "." * dots + " "), ("value", value)]

def panel():
    rule = "─" * (PANEL_W - len(HOST) - 1)
    return [[("host", HOST + " "), ("dim", rule)]] + list(rows())

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def svg(theme):
    c = THEMES[theme]
    art_w = max(len(l) for l in ART)
    cols, lines = art_w + GAP + PANEL_W, max(len(ART), len(panel()))
    w, h = round(cols * CW) + PAD * 2, lines * LINE_H + PAD * 2
    px = PAD + (art_w + GAP) * CW
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}" font-family="ui-monospace,SFMono-Regular,'
           f'Menlo,Consolas,&quot;Liberation Mono&quot;,monospace" '
           f'font-size="{FONT_PX}">']
    def text(x, i, runs):
        n = sum(len(t) for _, t in runs)
        y = PAD + i * LINE_H + FONT_PX
        # textLength pins the run to an exact width, so a monospace font with
        # a different advance ratio cannot push the panel out of the viewBox.
        spans = "".join(f'<tspan fill="{c[k]}">{esc(t)}</tspan>' for k, t in runs)
        out.append(f'<text x="{x:.1f}" y="{y}" xml:space="preserve" '
                   f'textLength="{n * CW:.1f}" lengthAdjust="spacing">{spans}</text>')
    for i, line in enumerate(ART):
        text(PAD, i, [("art", line.rstrip())])
    for i, line in enumerate(panel()):
        text(px, i, line)
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
    alt = " / ".join(f"{k}: {v}" for k, v in DATA)
    w = round((max(len(l) for l in ART) + GAP + PANEL_W) * CW) + PAD * 2
    files["README.md"] = README.format(alt=esc(f"{HOST} - {alt}"), w=w)
    return files

if "--live" in sys.argv:
    for i, (k, _) in enumerate(DATA):
        if k == "Lang":
            DATA[i] = ("Lang", lang_from_api())

files = build()
if "--check" in sys.argv:
    stale = [n for n, t in files.items() if (HERE / n).read_text() != t]
    sys.exit(f"stale, re-run render.py: {', '.join(stale)}" if stale else 0)
for n, t in files.items():
    (HERE / n).write_text(t)
    print(f"wrote {n}", file=sys.stderr)
