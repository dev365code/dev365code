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
CHIPS = [("iiRDS", 80), ("VDI 2770", 106), ("AAS", 64)]
LANGS = [  # two rows of four; column starts are fixed so the rows align like a table
    [("DE", "#7da7cf", "Offline geprüft"), ("FR", "#7db8cf", "Validé hors ligne"),
     ("IT", "#7dc7bd", "Convalidato offline"), ("NL", "#8cc79d", "Offline gevalideerd")],
    [("PL", "#b3c583", "Zweryfikowano offline"), ("CS", "#d4bd7a", "Ověřeno offline"),
     ("KO", "#ddab74", "오프라인 검증"), ("JA", "#d99a86", "オフラインで検証")],
]
COLX = [90, 309, 493, 692]   # measured column widths, block centred on 470

def langrow(items, y):
    out = []
    for (code, col, txt), x in zip(items, COLX):
        out.append(
            f'<rect x="{x}" y="{y-11}" width="30" height="17" rx="3" fill="{col}"/>'
            f'<text x="{x+15}" y="{y}" font-family="{MONO}" font-size="11" font-weight="700" '
            f'fill="#10151a" text-anchor="middle" letter-spacing="0.5">{code}</text>'
            f'<text x="{x+38}" y="{y}" font-family="{SANS}" font-size="14.5" fill="#9aa8b3">{txt}</text>')
    return "".join(out)

def chips_svg():
    total = sum(w for _, w in CHIPS) + 10 * (len(CHIPS) - 1)
    x, out = CX - total / 2, []
    for label, wd in CHIPS:
        out.append(f'<rect x="{x:.0f}" y="338" width="{wd}" height="28" rx="5" fill="none" '
                   f'stroke="rgba(143,184,221,.45)"/>'
                   f'<text x="{x+wd/2:.0f}" y="357" font-family="{MONO}" font-size="13.5" '
                   f'fill="#cfe0ef" text-anchor="middle">{label}</text>')
        x += wd + 10
    return "".join(out)


import math as _m
def _smear():
    segs, N, R, SPAN = [], 48, 57, 94.0
    C = 2 * _m.pi * R
    seg = C * (SPAN / 360.0) / N
    for i in range(N):
        t = (i + 0.5) / N
        op = 0.55 * (1 - abs(t - 0.5) * 2)
        off = -C * (SPAN / 360.0) * i / N
        segs.append('<circle cx="470" cy="100" r="57" fill="none" stroke="#ffeede" '
                    f'stroke-opacity="{op:.3f}" stroke-width="18" '
                    f'stroke-dasharray="{seg:.2f} {C - seg:.2f}" stroke-dashoffset="{off:.2f}"/>')
    return "".join(segs)
SMEAR = _smear()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="Standards, judged offline — AI proposes, rules judge, people decide">
<defs>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#2f5d8a" stop-opacity=".30"/><stop offset="100%" stop-color="#2f5d8a" stop-opacity="0"/></radialGradient>
<filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="softer"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="smear" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<rect width="940" height="470" fill="#0b0f14"/>
<path d="{grid_path()}" fill="none" stroke="rgba(198,212,224,0.075)" stroke-width="1"/>
<circle cx="470" cy="100" r="230" fill="url(#halo)"/>
<circle cx="470" cy="100" r="58" fill="none" stroke="#8fb8dd" stroke-opacity=".28" stroke-width="7" filter="url(#softer)"/>
<circle cx="470" cy="100" r="51" fill="#03050a"/>
<circle cx="470" cy="100" r="57" fill="none" stroke="#ffeede" stroke-opacity=".45" stroke-width="2" filter="url(#soft)"/>
<g filter="url(#smear)">
{SMEAR}
<animateTransform attributeName="transform" type="rotate" from="0 470 100" to="360 470 100" dur="16s" repeatCount="indefinite"/></g>
<text x="470" y="208" font-family="{MONO}" font-size="13" letter-spacing="3.4" fill="#93a1ad" text-anchor="middle">{KICKER}</text>
<text x="470" y="252" font-family="{SANS}" font-size="40" font-weight="700" fill="#e8edf2" text-anchor="middle">{TITLE[0]}<tspan fill="#8fb8dd">{TITLE[1]}</tspan></text>
<text x="470" y="290" font-family="{MONO}" font-size="19" font-weight="700" fill="#e8edf2" text-anchor="middle">{PUNCH[0]}<tspan fill="#8fb8dd">{PUNCH[1]}</tspan>{PUNCH[2]}</text>
<text x="470" y="319" font-family="{SANS}" font-size="16.5" fill="#c6d2dc" text-anchor="middle">{MARKET[0]}<tspan fill="#e8edf2" font-weight="600">{MARKET[1]}</tspan></text>
{chips_svg()}
{langrow(LANGS[0], 404)}
{langrow(LANGS[1], 430)}
</svg>'''
open('assets/hero.svg', 'w', encoding='utf-8').write(svg)
print("assets/hero.svg regenerated,", len(svg) // 1024, "KB")
