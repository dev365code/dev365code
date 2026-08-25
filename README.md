<!-- profile:start (rendered by render.py -- edit render.py, not this block) -->
<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="profile-dark.svg?v=2dd5efe9c3">
    <img alt="dev365code - OS: macOS 26.5.1, Linux / Shell: zsh / Editor: VS Code / Location: Seoul, KR / Languages.Programming: Python, Java, JavaScript / Languages.Real: Korean, English / Hobbies: algorithmic trading, jigsaw puzzles / iirds-validate: 185 rules, offline, Apache-2.0 / document AI: structure out of PDFs / Email: zero8004paz@gmail.com / GitHub: dev365code / Commits: 658 (456 in 2026) / Latest push: vdi2770-validate, 2026-08-25" src="profile-light.svg?v=b35170790e" width="1070">
  </picture>
</div>
<!-- profile:end -->

---

## Referees for industrial documentation standards

Machine documentation runs on standards — **iiRDS**, **VDI 2770**, the
**AAS submodel templates** — and almost none of them ship an open, offline
conformance checker. This account builds that layer: validators that say
*what* is wrong, *where the specification says so*, and *how to fix it*.
Verdicts are free, forever.

### Sixty seconds

```bash
pip install iirds-validate
iirdsv check manual.iirds        # every finding cites the clause and carries a remedy
iirdsv rules M11 -v              # what a rule enforces, its source, its fix
```

Nothing leaves your machine. There is no server.

### What exists

| standard | tool | |
|---|---|---|
| iiRDS 1.3 — packages, metadata graph, content | [**iirds-validate**](https://github.com/dev365code/iirds-validate) | [![PyPI](https://img.shields.io/pypi/v/iirds-validate)](https://pypi.org/project/iirds-validate/) |
| VDI 2770 — documentation containers | [**vdi2770-validate**](https://github.com/dev365code/vdi2770-validate) | [![PyPI](https://img.shields.io/pypi/v/vdi2770-validate)](https://pypi.org/project/vdi2770-validate/) |
| AAS submodels — instances against IDTA templates | [**aas-submodel-validate**](https://github.com/dev365code/aas-submodel-validate) | public, pre-release |
| iiRDS read/write | [**iirds**](https://github.com/dev365code/iirds) (SDK) | [![PyPI](https://img.shields.io/pypi/v/iirds)](https://pypi.org/project/iirds/) |
| the standards themselves — templates, releases, calls | [**standards-watch**](https://github.com/dev365code/standards-watch) | [RSS](https://raw.githubusercontent.com/dev365code/standards-watch/main/feed.xml) |

### How they are built

- Every rule cites the clause it enforces. Every fixture that once caught
  something stays as a regression.
- Coverage is measured against the *specification*, not the rule catalogue.
  iirds-validate maps [19 of 314](https://github.com/dev365code/iirds-validate/blob/main/docs/scope.md)
  absolute obligations today and says so in writing — "no findings" is not
  "conformant".
- Offline by construction. Rules are the source of truth; generated
  artefacts are regenerated, never hand-edited.

Not affiliated with the iiRDS Consortium, tekom, VDI or IDTA — the names
are used descriptively.
