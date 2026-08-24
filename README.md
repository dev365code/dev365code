## Conformance infrastructure for industrial documentation standards

Manufacturing runs on standards for machine documentation — **iiRDS**,
**VDI 2770**, the **AAS submodels** — yet almost none of them have an
open, offline referee. I build that layer: validators that tell you
*what* is broken and *how to fix it*, libraries to read and write the
containers, and a daily watch on the ecosystem. Verdicts are free,
forever.

| | | |
|---|---|---|
| [**iirds-validate**](https://github.com/dev365code/iirds-validate) | 185-rule offline validator + 138 differentially-tested SHACL shapes for iiRDS | [![PyPI](https://img.shields.io/pypi/v/iirds-validate)](https://pypi.org/project/iirds-validate/) |
| [**vdi2770-validate**](https://github.com/dev365code/vdi2770-validate) | Offline conformance checker for VDI 2770 documentation containers | [![PyPI](https://img.shields.io/pypi/v/vdi2770-validate)](https://pypi.org/project/vdi2770-validate/) |
| [**iirds**](https://github.com/dev365code/iirds) | Read/write SDK for iiRDS packages, held in stewardship for the ecosystem | [![PyPI](https://img.shields.io/pypi/v/iirds)](https://pypi.org/project/iirds/) |
| [**standards-watch**](https://github.com/dev365code/standards-watch) | Daily automated watch on the standards, their templates and funding calls | [RSS](https://raw.githubusercontent.com/dev365code/standards-watch/main/feed.xml) |

Every claim in these repositories is held by a test; every gate that
caught something is on the record. Not affiliated with the iiRDS
Consortium, tekom, VDI or IDTA — the names are used descriptively.
