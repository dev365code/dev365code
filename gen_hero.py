#!/usr/bin/env python3
"""Generate assets/hero.svg — the black-hole banner.

The picture is mathematics, not an image file: a square grid pulled toward a
gravity well (pure contraction, no theatrics), an event-horizon ring with one
slow hotspot, and the words. Regenerate after editing; the SVG is the output,
this file is the source of truth.

    python3 gen_hero.py            # writes assets/hero.svg
"""
import math

CX, CY, W, H = 470.0, 100.0, 940, 470
A, S = 0.55, 165.0            # contraction, falloff radius
EXT = 182                     # grid extended past the frame so the top stays filled

def warp(x, y):
    dx, dy = x - CX, y - CY
    r = math.hypot(dx, dy)
    g = 1.0 - A * math.exp(-(r / S) ** 2)
    return CX + dx * g, CY + dy * g

def grid_path():
    parts = []
    for xi in range(-EXT, W + EXT + 1, 26):
        pts = [warp(xi, yy) for yy in range(-EXT, H + 1, 10)]
        parts.append('M' + 'L'.join(f'{px:.1f},{py:.1f}' for px, py in pts))
    for yi in range(-EXT, H + 1, 26):
        pts = [warp(xx, yi) for xx in range(-EXT, W + EXT + 1, 10)]
        parts.append('M' + 'L'.join(f'{px:.1f},{py:.1f}' for px, py in pts))
    return " ".join(parts)

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = ("-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,"
        "'Apple SD Gothic Neo','Malgun Gothic','Hiragino Sans',sans-serif")

KICKER = "INDUSTRIAL DOCUMENT STANDARDS"
TITLE = ("Standards, ", "judged offline.")
PUNCH = ("AI proposes. ", "Rules judge.", " People decide.")
MARKET = ("Machines enter Europe on paperwork. ", "These tools judge the paperwork.")
CHIPS = [("iiRDS", 76), ("VDI 2770", 100), ("AAS", 60)]
LANGS = [  # two rows of four; column starts are fixed so the rows align like a table
    [("DE", "#7da7cf", "Offline geprüft"), ("FR", "#7db8cf", "Validé hors ligne"),
     ("IT", "#7dc7bd", "Convalidato offline"), ("NL", "#8cc79d", "Offline gevalideerd")],
    [("PL", "#b3c583", "Zweryfikowano offline"), ("CS", "#d4bd7a", "Ověřeno offline"),
     ("KO", "#ddab74", "업로드 없이 판정"), ("JA", "#d99a86", "オフラインで検証")],
]
COLX = [122, 328, 534, 742]

def langrow(items, y):
    out = []
    for (code, col, txt), x in zip(items, COLX):
        out.append(
            f'<rect x="{x}" y="{y-11}" width="26" height="15" rx="3" fill="{col}"/>'
            f'<text x="{x+13}" y="{y}" font-family="{MONO}" font-size="9.5" font-weight="700" '
            f'fill="#10151a" text-anchor="middle" letter-spacing="0.5">{code}</text>'
            f'<text x="{x+34}" y="{y}" font-family="{SANS}" font-size="12" fill="#93a1ad">{txt}</text>')
    return "".join(out)

def chips_svg():
    total = sum(w for _, w in CHIPS) + 10 * (len(CHIPS) - 1)
    x, out = CX - total / 2, []
    for label, wd in CHIPS:
        out.append(f'<rect x="{x:.0f}" y="338" width="{wd}" height="26" rx="5" fill="none" '
                   f'stroke="rgba(143,184,221,.45)"/>'
                   f'<text x="{x+wd/2:.0f}" y="355" font-family="{MONO}" font-size="12.5" '
                   f'fill="#cfe0ef" text-anchor="middle">{label}</text>')
        x += wd + 10
    return "".join(out)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="Standards, judged offline — AI proposes, rules judge, people decide">
<defs>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2f5d8a" stop-opacity=".30"/><stop offset="100%" stop-color="#2f5d8a" stop-opacity="0"/></radialGradient>
<filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="softer"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<rect width="940" height="470" fill="#0b0f14"/>
<path d="{grid_path()}" fill="none" stroke="rgba(198,212,224,0.075)" stroke-width="1"/>
<circle cx="470" cy="100" r="230" fill="url(#halo)"/>
<circle cx="470" cy="100" r="58" fill="none" stroke="#8fb8dd" stroke-opacity=".5" stroke-width="9" filter="url(#softer)"/>
<circle cx="470" cy="100" r="51" fill="#03050a"/>
<circle cx="470" cy="100" r="57" fill="none" stroke="#ffeede" stroke-opacity=".85" stroke-width="2.4" filter="url(#soft)"/>
<g><circle cx="470" cy="100" r="57" fill="none" stroke="#fff1e0" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="42 316" filter="url(#soft)"/>
<animateTransform attributeName="transform" type="rotate" from="0 470 100" to="360 470 100" dur="16s" repeatCount="indefinite"/></g>
<text x="470" y="208" font-family="{MONO}" font-size="12" letter-spacing="3.2" fill="#93a1ad" text-anchor="middle">{KICKER}</text>
<text x="470" y="252" font-family="{SANS}" font-size="37" font-weight="700" fill="#e8edf2" text-anchor="middle">{TITLE[0]}<tspan fill="#8fb8dd">{TITLE[1]}</tspan></text>
<text x="470" y="290" font-family="{MONO}" font-size="17" font-weight="700" fill="#e8edf2" text-anchor="middle">{PUNCH[0]}<tspan fill="#8fb8dd">{PUNCH[1]}</tspan>{PUNCH[2]}</text>
<text x="470" y="319" font-family="{SANS}" font-size="14.5" fill="#c6d2dc" text-anchor="middle">{MARKET[0]}<tspan fill="#e8edf2" font-weight="600">{MARKET[1]}</tspan></text>
{chips_svg()}
{langrow(LANGS[0], 404)}
{langrow(LANGS[1], 430)}
</svg>'''
open('assets/hero.svg', 'w', encoding='utf-8').write(svg)
print("assets/hero.svg regenerated,", len(svg) // 1024, "KB")
