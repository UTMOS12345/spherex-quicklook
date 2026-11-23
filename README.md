# spherex-quicklook

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-green)](LICENSE)
[![tests](https://github.com/UTMOS12345/spherex-quicklook/actions/workflows/tests.yml/badge.svg)](https://github.com/UTMOS12345/spherex-quicklook/actions/workflows/tests.yml)

**A quick-look library for NASA SPHEREx images.** Give it a star name or a sky position and
it finds the SPHEREx frames in the IRSA archive, downloads small cutouts, cleans them (ZODI
subtracted, flagged pixels masked), stacks each visit onto one sky grid, and returns what you
can look at directly: per-visit pictures and difference images, an animated GIF, Gaia DR3 and
CatWISE2020 overlays, light curves and 102-channel spectra measured from the images, each
table with its caveats written out in words.

The distribution is called `spherex-quicklook`; the package you import is `spherex` (as with
scikit-learn and `sklearn`). It is the library behind the
[SPHEREx Flipbook app (paramost)](https://github.com/UTMOS12345/spherex_project).

## Install

```
pip install git+https://github.com/UTMOS12345/spherex-quicklook.git@v1.0.0
```

Python 3.10 or newer. No web framework is installed: the library needs only astropy,
astroquery, photutils, reproject, numpy, scipy, matplotlib, platformdirs and requests.

## Example

```python
from spherex import api

api.set_style()                                     # one look for every figure
print(api.resolve("WISE 0855"))                     # position, proper motion
print(api.visits("WISE 0855"))                      # visits, frames per detector, releases
open("wise0855.gif", "wb").write(api.flipbook("WISE 0855", detector="D6", fov=4.0))
fig, lc = api.light_curve_figure("WISE 0855", band=4.5, tol=0.02)
fig.savefig("wise0855_light_curve.png")
print(lc.meta.get("warning"))                       # the caveats, in words
fig, spec = api.spectrum_figure("WISE 0855")        # latest visit, 102 channels
fig.savefig("wise0855_spectrum.png")
```

The first call for a new target downloads its images (minutes); after that everything comes
from the cache in seconds. [docs/API.md](docs/API.md) describes every function, its inputs and
outputs, the warnings, progress callbacks and errors; the
[tutorial notebook](notebooks/tutorial.ipynb) walks through every view.

**matplotlib:** the library never chooses a backend. In a script without a display matplotlib
uses Agg by itself. An app that draws from threads (a web server, Streamlit) should select Agg
before importing `spherex` (`MPLBACKEND=Agg`).

## The cache

Downloads, frame lists, catalogue cones and saved results go to `SPHEREX_CACHE` if it is set,
else to the per-user cache folder: `~/.cache/paramost` on Linux, `~/Library/Caches/paramost`
on macOS, `%LOCALAPPDATA%\paramost\Cache` on Windows. It is named after the app because the
library first shipped inside it and its users already have gigabytes there; set
`SPHEREX_CACHE=/any/folder` to use another (renaming the default is a candidate for 2.0).
`api.cache_root()` says which folder is in use. `SPHEREX_CACHE_MAX_GB`, `SPHEREX_CACHE_POLICY`,
`SPHEREX_CACHE_TTL_DAYS` and `SPHEREX_FRAME_CACHE_MAX_GB` cap it; see docs/API.md.

## Stability

From 1.0.0 the library follows [semantic versioning](https://semver.org) for its public
interface, which is:

- everything in `spherex.api` whose name does not start with `_`, as documented in
  [docs/API.md](docs/API.md): function names, arguments, return types, table columns and units;
- `spherex.__version__`;
- the environment variables `SPHEREX_CACHE`, `SPHEREX_DEMO`, `SPHEREX_CACHE_*`,
  `SPHEREX_FRAME_CACHE*`, `SPHEREX_WORKERS` and `SPHEREX_DOWNLOAD_WORKERS_MAX`;
- the layout of the cache folder, so an existing cache keeps working across 1.x.

Within 1.x these change only in backward-compatible ways; anything that breaks them waits for
2.0. Everything else is internal and may change in any release: the other modules
(`spherex.net`, `spherex.download`, `spherex.frames`, `spherex.framecache`, `spherex.workers`,
`spherex.results`, ...), the names re-exported at the top of `spherex`, and anything starting
with `_`. The app uses only `spherex.api`.

Scientific results (stacks, photometry, spectra) are reproducible: a release that changes any
of them on purpose says so in the [CHANGELOG](CHANGELOG.md) and raises `RESULTS_VERSION`, so
results saved by an older version are recomputed rather than reused.

## Development

```
git clone https://github.com/UTMOS12345/spherex-quicklook.git
cd spherex-quicklook
python -m venv .venv && . .venv/bin/activate
pip install -e ".[test]"
pytest -q tests                                     # unit tests, no network
```

Working on the app at the same time: clone both side by side and install this one editable
into the app's environment (`pip install -e ../spherex-quicklook`); see the app's README.

## Credits

- **SPHEREx** data from the NASA/IPAC Infrared Science Archive (**IRSA**), operated by
  Caltech/IPAC under contract with NASA.
- **Gaia DR3**, from the ESA mission Gaia, processed by the Gaia Data Processing and Analysis
  Consortium (Gaia Collaboration, Vallenari et al. 2023, A&A 674, A1).
- **CatWISE2020** (Marocco et al. 2021, ApJS 253, 8), via IRSA.
- **SkyBoT**, IMCCE, Observatoire de Paris (Berthier et al. 2006).
- **SIMBAD** and the **Sesame** name resolver, CDS, Strasbourg (Wenger et al. 2000).
- **Software:** astropy, astroquery, photutils, reproject, numpy, scipy, matplotlib and
  platformdirs.

Written by UTMOS12345 ([@UTMOS12345](https://github.com/UTMOS12345)) and Jumanov Shavkat
([@ShavkatJumanov](https://github.com/ShavkatJumanov)) for the NASA Space Apps Challenge 2026,
Planet X and SPHEREx. Please cite it with [CITATION.cff](CITATION.cff).

**AI assistance:** much of the code, tests and documentation was written with Claude Code
(Anthropic), under the team's direction.

Licensed under [BSD-3-Clause](LICENSE).
