# Peak Pet Supply — brand asset package

**Source of truth is vector.** The site's `img/logo-*.svg` files only *wrap* a 1096 × 536 PNG of the emblem; this package rebuilds the emblem (dog on the peak) as true vector with potrace and carries the already-vector Montserrat wordmark outlines over unchanged. Every file here is generated from `_build/geometry.json` — nothing is hand-exported. Change a value, run `_build/regen.sh`, and every deliverable agrees.

Package built 2026-09-16 (v1). Lives in the site repo at `brand/pps-brand/`; `audio/`, `renders/` and trace intermediates are git-ignored (the repo is public GitHub Pages).

| Folder | Contents |
|---|---|
| `masters/` | 38 SVG masters — `pps-lockup-vertical*` (light / on-dark / outline / on-navy / on-navy-color / on-cream / mono black-white-navy-blue-gold), `pps-lockup-horizontal*` (boxed) + `-type*` (nav/email), `pps-mark*`, `pps-dog*`, `pps-wordmark*` (boxed / unboxed / horizontal), `pps-benchmark-gold/-bronze` (secondary mark) |
| `png/` | lockups at 1000 / 2000 / 4000 w, marks at 1024 / 2048 / 4096, everything else at 2000 w |
| `icons/` | `pps-icon-<16…1024>.png`, `favicon.ico`, `apple-touch-icon-180.png`, `ios-app-icon-1024.png`, maskable (60 %), cream tile, **`pps-favicon-dog*` + `favicon-dog.ico`** (the dog alone reads at 16 px; the full emblem does not), benchmark icon |
| `social/` | avatars (navy / cream / dog / benchmark), YouTube 2560×1440, X 1500×500, Facebook 1640×624, LinkedIn 1584×396, OG 1200×630, Instagram post + story — SVG + PNG |
| `ae-kit/` | `parts/` (layers already placed in 1920×1080 + a 1080×1920 vertical, `registration.json`, `timeline.json`), `intro-previz.html` ("Summit", tuning panel), `PPS-MOTION-SPEC.md` |
| `audio/` | the six PPS clips as WAV (git-ignored; originals in `~/Music/Piscean Produtions ♓️/`) |
| `_build/` | `geometry.py` → `geometry.json` → `lib.py` → `export.py` / `ae.py` / `gen_previz.py` / `gen_sheet.py` / `contact.py`; `contact.jpg` and `split-proof.png` proofs; `regen.sh` |
| `brand-sheet.html` | self-contained sheet: marks, color, clearspace, construction, type, do/don't, motion, file map |

## Locked values
- **Colors** — navy `#0E2433` (ground, icons, type on light) · brand blue `#10689A` (emblem on light) · gold `#F6C808` (wordmark box) · off-white `#F8F8F8` (emblem + type on dark) · cream `#f2efe9` (light ground) · forest `#161b1b` (site header/footer). Site-only: link gold `#B8860B`, button gold `#E5B94E`.
- **Lockup space** 548 × 486 units (the site's viewBox). Emblem bbox `[46, 26.25, 506.75, 256.25]`; dog `[170.25, 26.25, 331, 178.25]`; summit at `(313.5, 137.75)`; box `x 19.5 y 269.5 w 509 h 209 rx 14`, outline stroke 3.
- **Wordmark sets** — LIGHT (thinner weights, text on the gold box, from `logo-final.svg`) and DARK (heavier, from `logo-white.svg`; used for outline + dark grounds). Both are shipped outlines; the scheme picks the set.
- **Horizontal lockup** — box height 80 % of emblem height, gap 10 %. Type lockup — type 42 %, gap 10 %.
- **Clearspace** X = height of the dog on every side. Minimum widths on the brand sheet.
- **Trace recipe** — alpha → 2× zoom → gaussian 1.2 (`mode='constant'`) → threshold 0.5 → potrace `-a 1.0 -O 0.3 -t 30`; dog / mountain and left / centre / right peaks by watershed on the distance transform (cores = opening, disk r 50 px). Cuts land at the paws and the ridge saddles.

## Naming
`pps-<part>-<variant>-<size>` — lowercase, hyphens. `-on-dark` = transparent file recolored for dark grounds; `-on-navy` / `-on-cream` = filled ground; `-on-navy-color` = offwhite emblem + gold box (hero / social / ident scheme).

## Regenerate
```bash
brew install librsvg potrace
python3 -m venv .venv && .venv/bin/pip install -r _build/requirements.txt
PY=.venv/bin/python _build/regen.sh        # geometry → export → ae → previz → sheet → contact.jpg
```
Then open `_build/contact.jpg` and look at it before shipping anything.

## Motion — "Summit"
Previz: run the `pps-previz` launch config (serves this folder on :8767) and open `http://localhost:8767/ae-kit/intro-previz.html?tune=1`. Every audio start, gain and visual hit is a slider; 📋 copies the settings JSON — paste it back and the defaults get baked into `_build/gen_previz.py`, which rewrites `timeline.json` and the spec. Order of operations: previz → lock → parts + spec → `build-comp.jsx` (not started until the previz is approved).

## Site
The site still references `img/logo-white.svg` etc. Once this package is approved, swap those for `masters/pps-lockup-vertical-on-dark.svg` (header/footer), `icons/favicon.ico` + `icons/pps-favicon-dog-*.png` (favicons), and `social/pps-og-1200x630.png` (share card) — all vector-true and smaller than the PNG-wrapped files.
