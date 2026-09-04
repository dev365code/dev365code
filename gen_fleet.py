#!/usr/bin/env python3
"""Generate assets/fleet-*.svg — one dark instrument row per tool.

Markdown tables cannot hold this design (the retired renderer's own lesson),
so each row is an SVG the README wraps in a link. Numbers here are re-measured
and regenerated on every release; this file is the source of truth.

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

W, H = 940, 64
for fname, name, desc, chip, chipcol, status, frac, faint in ROWS:
    chip_w = 10 + int(len(chip) * 6.6)
    name_w = int(len(name) * 8.6)
    fill_op = ' fill-opacity=".35"' if faint else ''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{name} — {status}">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="#12161a" stroke="#252b30" stroke-width="1.5"/>
<text x="24" y="29" font-family="{MONO}" font-size="15" font-weight="700" fill="#7da7cf">{name}</text>
<text x="24" y="46" font-family="{MONO}" font-size="10" letter-spacing="0.6" fill="#7d8a99">PyPI · Apache-2.0</text>
<rect x="{28+name_w}" y="15" width="{chip_w}" height="17" rx="3" fill="{chipcol}"/>
<text x="{28+name_w+chip_w/2:.0f}" y="27" font-family="{MONO}" font-size="10.5" font-weight="600" fill="#ffffff" text-anchor="middle">{chip}</text>
<text x="316" y="37" font-family="{SANS}" font-size="13.5" fill="#d8dfe5">{desc}</text>
<text x="916" y="26" font-family="{MONO}" font-size="11" fill="#93a1ad" text-anchor="end">{status}</text>
<rect x="712" y="36" width="204" height="7" rx="3.5" fill="#20262a"/>
<rect x="712" y="36" width="{204*frac:.0f}" height="7" rx="3.5" fill="#7da7cf"{fill_op}/>
</svg>'''
    open(f'assets/fleet-{fname}.svg', 'w', encoding='utf-8').write(svg)
    print(f'assets/fleet-{fname}.svg')
