#!/usr/bin/env python3
"""Generate assets/fleet-*.svg — one dark instrument row per tool.

Two-band layout so nothing can collide by construction: band one holds the
name, version chip and status text; band two holds the description on the
left and the gauge on the right, in separate horizontal territories.
Regenerated on every release; this file is the source of truth.

    python3 gen_fleet.py
"""
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"

ROWS = [
    ("iirds", "iirds", "Judges iiRDS 1.3 documentation packages — validator + reader, one install",
     "v0.5.0", "#2f6fb3", "77 / 280 obligations · a floor", 0.275, False),
    ("vdi2770-validate", "vdi2770-validate", "Judges VDI 2770 documentation containers for machine delivery",
     "v0.6.1", "#2f6fb3", "obligation index: in the making", 0.06, False),
    ("aas-submodel-validate", "aas-submodel-validate", "Judges AAS submodels against IDTA templates",
     "v0.1.0 · new", "#3d8b57", "template packs: 3 shipped", 0.12, False),
    ("standards-watch", "standards-watch", "Watches the standards themselves — releases, errata, template changes",
     "daily", "#a8721c", "observation, on the record", 1.0, True),
]

W, H = 940, 76
CW_MONO15 = 9.4          # generous per-char width for the 15px mono name
for fname, name, desc, chip, chipcol, status, frac, faint in ROWS:
    name_w = int(len(name) * CW_MONO15)
    chip_w = 16 + int(len(chip) * 7.0)
    chip_x = 24 + name_w + 12
    fill_op = ' fill-opacity=".35"' if faint else ''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{name} — {status}">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="#12161a" stroke="#252b30" stroke-width="1.5"/>
<text x="24" y="31" font-family="{MONO}" font-size="15.5" font-weight="700" fill="#7da7cf">{name}</text>
<rect x="{chip_x}" y="16" width="{chip_w}" height="20" rx="4" fill="{chipcol}"/>
<text x="{chip_x + chip_w/2:.0f}" y="30" font-family="{MONO}" font-size="11.5" font-weight="600" fill="#ffffff" text-anchor="middle">{chip}</text>
<text x="916" y="30" font-family="{MONO}" font-size="12" fill="#93a1ad" text-anchor="end">{status}</text>
<text x="24" y="59" font-family="{SANS}" font-size="14" fill="#c9d2da">{desc}</text>
<rect x="732" y="51" width="184" height="8" rx="4" fill="#20262a"/>
<rect x="732" y="51" width="{184*frac:.0f}" height="8" rx="4" fill="#7da7cf"{fill_op}/>
</svg>'''
    open(f'assets/fleet-{fname}.svg', 'w', encoding='utf-8').write(svg)
    print(f'assets/fleet-{fname}.svg')
