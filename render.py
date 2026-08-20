#!/usr/bin/env python3
"""Render the profile: README.md and the two SVGs it points at.

    python render.py            # rebuild from ROWS, overlaid with live.json
    python render.py --live      # re-derive live.json from the API first
    python render.py --check     # fail if the committed files have drifted

ROWS holds a value for every row so the file renders with no network at all.
What an API knows better is re-derived into live.json and overlaid on top, in
its own file rather than edited back into ROWS, so --check stays meaningful
after the scheduled job has run.

Columns are computed here, never typed, so a value can change length without
anyone re-counting spaces. It is an SVG because a fenced code block cannot be
centred -- align=center resolves to text-align, which centres each line inside
the <pre> separately and tears the ASCII apart -- and because GitHub does not
render ANSI colour in Markdown.
"""
import json, os, pathlib, sys, urllib.request

HERE = pathlib.Path(__file__).parent
USER = "dev365code"
PANEL_W = 58
GAP_PX = 44
FONT_PX, LINE_H, CW = 14, 20, 8.4
SCALE = float(os.environ.get("SCALE", 2.0))   # how much bigger the 365 runs
PAD = 26

HOST = "wooyong@lee"
ROWS = [
    ("row",  "OS",                    "macOS 26.5.1, Linux"),
    ("row",  "Host",                  "MacBook (Apple M5)"),
    ("row",  "Kernel",                "Darwin 25.5.0"),
    ("row",  "IDE",                   "VS Code 1.134.0"),
    ("row",  "Shell",                 "zsh"),
    ("row",  "Location",              "Seoul, KR"),
    ("gap",),
    ("row",  "Languages.Programming", "Python, Java, JavaScript"),
    ("row",  "Languages.Computer",    "HTML, CSS, JSON, YAML, RDF/XML"),
    ("row",  "Languages.Real",        "Korean, English"),
    ("gap",),
    ("row",  "Hobbies.Software",      "algorithmic trading, ASCII art"),
    ("row",  "Hobbies.Offline",       "jigsaw puzzles"),
    ("sect", "Projects"),
    ("row",  "iirds-validate",        "185 rules, offline, Apache-2.0"),
    ("row",  "document AI",           "structure out of PDFs"),
    ("sect", "Contact"),
    ("row",  "Email.Personal",        "zero8004paz@gmail.com"),
    ("row",  "GitHub",                USER),
    ("sect", "GitHub Stats"),
    ("row",  "Commits",               "541 (339 in 2026)"),
    ("row",  "Latest push",           "dev365code, 2026-08-20"),
]

# figlet "colossal", drawn at SCALE x the panel's type size
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

# Hermes orange is #F37021. On white it lands at 2.94:1, under WCAG AA, so the
# light theme keeps the hue and drops brightness to 75%, #BF581A (4.54:1).
THEMES = {
    "dark":  dict(art="#F37021", label="#F37021", value="#79c0ff",
                  dim="#3d444d", host="#e6edf3"),
    "light": dict(art="#BF581A", label="#BF581A", value="#0550AE",
                  dim="#afb8c1", host="#1f2328"),
}

def api(url):
    tok = os.environ.get("GITHUB_TOKEN")
    hdr = {"Authorization": f"Bearer {tok}"} if tok else {}
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers=hdr), timeout=30))

def graphql(query):
    tok = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))["data"]

def refresh():
    """Re-derive the rows an API knows better than a hand-edited file.

    Deliberately absent: stars, followers, repository count and lines of code.
    Stars and followers are currently numbers that argue against their owner.
    Lines of code is 65% private repositories, so nobody reading the profile
    could check it, and 877k over 541 commits reads as committed data rather
    than written code. The repository count lands at 6 here and 11 with a
    token that can see private repos, and neither number says anything.
    """
    out = {}
    repos, page = [], 1
    while True:
        got = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}")
        if not got:
            break
        repos += got
        page += 1
    own = [r for r in repos if not r["fork"]]

    tot = {}
    for r in own:
        for k, v in api(r["languages_url"]).items():
            tot[k] = tot.get(k, 0) + v
    if tot:
        out["Languages.Programming"] = ", ".join(
            sorted(tot, key=tot.get, reverse=True)[:3])

    newest = max(own, key=lambda r: r["pushed_at"])
    out["Latest push"] = f'{newest["name"]}, {newest["pushed_at"][:10]}'

    try:
        years = range(2019, 2027)
        q = "{user(login:\"%s\"){%s}}" % (USER, " ".join(
            f'y{y}:contributionsCollection(from:"{y}-01-01T00:00:00Z",'
            f'to:"{y}-12-31T23:59:59Z"){{totalCommitContributions '
            f'restrictedContributionsCount}}' for y in years))
        d = graphql(q)["user"]
        per = {int(k[1:]): v["totalCommitContributions"]
                     + v["restrictedContributionsCount"] for k, v in d.items()}
        this = max(per)
        out["Commits"] = f"{sum(per.values()):,} ({per[this]:,} in {this})"
    except Exception as e:                       # keep the committed value
        print(f"commits: kept, {e}", file=sys.stderr)
    return out

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

def dims():
    art_w = max(len(l) for l in ART) * CW * SCALE
    art_h = len(ART) * LINE_H * SCALE
    rows_ = panel()
    body_h = max(art_h, len(rows_) * LINE_H)
    return art_w, art_h, rows_, body_h

def svg(theme):
    c = THEMES[theme]
    art_w, art_h, rows_, body_h = dims()
    w = round(art_w + GAP_PX + PANEL_W * CW) + PAD * 2
    h = round(body_h) + PAD * 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}" font-family="ui-monospace,SFMono-Regular,'
           f'Menlo,Consolas,&quot;Liberation Mono&quot;,monospace" '
           f'font-size="{FONT_PX}">']

    def text(x, y, runs, scale=1.0):
        chars = sum(len(t) for _, t in runs)
        if not chars:
            return
        # textLength pins the run to an exact width, so a monospace fallback
        # with a different advance ratio cannot push anything out of place.
        spans = "".join(f'<tspan fill="{c[k]}">{esc(t)}</tspan>' for k, t in runs)
        fs = f' font-size="{FONT_PX * scale:g}"' if scale != 1 else ""
        out.append(f'<text x="{x:.1f}" y="{y:.1f}"{fs} xml:space="preserve" '
                   f'textLength="{chars * CW * scale:.1f}" '
                   f'lengthAdjust="spacing">{spans}</text>')

    top = PAD + (body_h - art_h) / 2
    for i, line in enumerate(ART):
        text(PAD, top + (i + 1) * LINE_H * SCALE - 4 * SCALE,
             [("art", line.rstrip())], SCALE)
    top = PAD + (body_h - len(rows_) * LINE_H) / 2
    for i, line in enumerate(rows_):
        text(PAD + art_w + GAP_PX, top + i * LINE_H + FONT_PX, line)
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
    art_w, _, _, _ = dims()
    files = {f"profile-{t}.svg": svg(t) for t in THEMES}
    files["README.md"] = README.format(
        alt=esc("dev365code - " + " / ".join(
            f"{r[1]}: {r[2]}" for r in ROWS if r[0] == "row")),
        w=round(art_w + GAP_PX + PANEL_W * CW) + PAD * 2)
    return files

LIVE = HERE / "live.json"

if "--live" in sys.argv:
    LIVE.write_text(json.dumps(refresh(), indent=2, sort_keys=True) + "\n")

if LIVE.exists():
    fresh = json.loads(LIVE.read_text())
    ROWS[:] = [(r[0], r[1], fresh.get(r[1], r[2])) if r[0] == "row" else r
               for r in ROWS]

files = build()
if "--check" in sys.argv:
    stale = [n for n, t in files.items() if (HERE / n).read_text() != t]
    sys.exit(f"stale, re-run render.py: {', '.join(stale)}" if stale else 0)
for n, t in files.items():
    (HERE / n).write_text(t)
    print(f"wrote {n}", file=sys.stderr)
