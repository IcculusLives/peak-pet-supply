# Peak Pet Supply — "Summit" ident · motion spec v1 (draft, 2026-09-16)

**Status: previz draft — NOT locked.** Every number here is a slider in `intro-previz.html` (⚙︎ tune / `?tune=1`). Casey tunes by ear, 📋 copies the settings JSON, and the values get baked into `_build/gen_previz.py` → this spec + `parts/timeline.json` regenerate. No ExtendScript until the previz is approved.

Comp `PPS_Summit` · 1920 × 1080 · 30 fps · 435 f (14.50 s) · ground navy `#0E2433` · scheme: off-white emblem, gold box, off-white type (`masters/pps-lockup-vertical-on-navy-color.svg`). Vertical 1080 × 1920 set in `parts/10-full-lockup-vertical-1080x1920.svg`.

## Concept
The three peaks rise out of the ground line on the bed's grid. The dog drops from above and **lands on the summit on the 808** — squash, dust at the paws, a shockwave ring, the whole mountain thuds. The gold box slams in, PEAK pops, PET SUPPLY wipes on left→right, the lockup settles and breathes. One last pulse + flash near the end, then dead still.

## Audio (package `audio/`, WAV from `~/Music/Piscean Produtions ♓️/`; onsets = +6 dB RMS jumps above −30 dBFS)
| slot | file | length | cues inside the file (s) | v1 start | gain |
|---|---|---|---|---|---|
| bed | PPS_1pearl.wav | 14.58 | 0.82 1.33 1.79 2.13 2.49 2.75 3.25 3.48 4.41 4.66 5.17 5.63 5.97 6.33 6.59 7.09 7.32 7.56 8.25 8.49 8.96 9.47 9.80 10.17 … (peak −6.5 dB, tail to 14.42) | 0.00 | 0.60 |
| k808 | PPS_808wFB.wav | 1.01 | hit at 0.00 (peak −6.1 dB) | 2.49 | 0.90 |
| fb | PPS_FB_pearl.wav | 2.60 | 0.60 · 0.91 · 1.80 · 2.09 | 3.80 | 0.80 |
| two5 | PPS_2.5.wav | 1.11 | 0.50 | 5.39 | 0.70 |
| p2 | PPS_2.wav | 6.13 | 0.68 (then sustains to 5.88) | 8.30 | 0.55 |
| jj | PPS_jj_short.wav | 1.11 | 0.50 | 12.60 | 0.80 |

The wall clock is the master; every track (bed included) is scheduled off its own start slider, so the bed can move too.

## Registration (comp px, from `parts/registration.json`; lockup 860 px tall, scale 1.895317)
| part | bbox [x0 y0 x1 y1] | center |
|---|---|---|
| lockup | 474.8 110.0 1445.2 970.0 | 960.0, 540.0 |
| emblem | 527.9 110.0 1401.1 545.9 | 964.5, 328.0 |
| dog | 763.4 110.0 1068.0 398.1 | 915.7, 254.0 · paws at y 398.1 |
| summit | — | 1034.9, 321.3 |
| ground line | y = 545.9 | |
| box | 474.8 568.2 1445.2 970.0 | 960.0, 769.1 |
Left / center / right peaks and PEAK / PET SUPPLY bboxes: see registration.json.

## Frame table v1 (30 fps; `F` in timeline.json)
| frame (s) | layer | action | ease |
|---|---|---|---|
| 0 | wash | blue radial wash fades in over 40 f | ease-out |
| 25 (0.82) | mountain-left | scale-Y 0→1 about the ground line, 16 f, 5 % overshoot | ease-out → ease-in-out |
| 40 (1.33) | mountain-center | same | |
| 54 (1.79) | mountain-right | same | |
| 65 (2.16) | dog | appears 760 px above, falls 10 f (stretched 0.96 × 1.06) | ease-in (cubic) |
| 75 (2.49) | dog | **LANDS**: squash to 0.84 in 3 f, recover to 1.05 by 7 f, settle 1.0 at 10 f; dust puffs (2 ellipses, 18 f); white ring 40→1300 px (30 f) + gold ring; emblem thud 1.035 × 0.95 about ground (14 f); gold wash blink (16 f) | |
| 132 (4.40) | box | pop 1.22→1 in 9 f + ring | ease-out / ease-in-out |
| 141 (4.71) | PEAK | pop 1.30→1 in 11 f, opacity 3 f, ring | |
| 168 (5.60) | PET SUPPLY | clip wipe left→right 10 f | ease-out |
| 177 (5.89) | lockup | settle pulse +3 % (12 f) + ring; then breathe ±0.4 % at 2.4 s period | |
| 393 (13.10) | lockup | final pulse +4.5 % (16 f), flash 0.55→0 (20 f), two rings | |
| 408 (13.60) | — | dead still, hold to 435 | |

## Build notes (for later, after lock)
Parts are numbered in stack order: `00-bg`, `01–03` peaks (or `04-mountain` whole), `05-dog`, `06-box-gold`, `07-peak`, `08-pet-supply`, `09-full-lockup`. Anchor each layer at its registration center; peaks and the emblem thud anchor at the ground line (y 545.9), the dog at its paws (y 398.1). Rings/dust/flash = shape layers + solids. Follow the `after-effects-pipeline` doctrine (CSD `build-comp.jsx` as the template; ES3; re-fetch properties after `addProperty`; one KeyframeEase per dimension).

---
## v1.1 — Casey's audio placement baked (2026-09-16) + vocal effects
Starts (s): bed 0.00 · **PPS 2.5 2.49** (hit 0.17 in → 2.66) · **jj 4.40** (hit → 4.57; jj and 2.5 are byte-identical files) · **PPS 2 = VOCAL 5.89** · **FB pearl 11.59** (hits 12.19 / 12.50 / 13.39 / 13.68) · **808 11.96** (hit → 12.03). Gains bed .60 · 808 .92 · FB .80 · 2.5 .70 · PPS 2 .55 · jj .80.
Realigned hits: dog lands **2.60**, box slams **4.50**, final flash **12.03** (the 808), still **13.90**. Everything else as v1.

**Vocal analysis (PPS_2.wav, 250–3500 Hz RMS, file-relative):** syllables 0.24 0.48 0.68 1.12 1.31 | held note 1.32–3.50 | 3.59 3.95 4.34 4.73 5.08 5.37 | tail to 6.12. Absolute with start 5.89: 6.13 6.37 6.57 7.01 **7.20** | held **7.21–9.39** | 9.48 9.84 10.23 10.62 10.97 11.26 | 12.01. Level curve every 0.1 s is in `timeline.json → vocal.level_0.1s`.

**Vocal effects (window `voc_from`→`voc_to` inside the file, default 1.32→6.13 = 7.21→12.02 abs; all ride the PPS 2 start slider):**
| what | driver |
|---|---|
| Howl arcs — sound-wave arcs from the dog's snout (comp 1067.6, 144.4), tilted −18°, one every `voc_rate` frames | live voice level (arc size, weight, opacity) |
| Gold aura around the snout | voice level² × `voc_amt` |
| Dog swells (scale-Y +4.5 %, X +1.5 %) and the lockup breathes +1.2 % | voice level |
| Syllable bursts: 3 arcs (white / gold / white), PEAK bounce +7 %, box +2 %, gold ground blink | each syllable onset × `voc_syl` |
| Lock ticks on the four FB-pearl hits: box → PEAK → PET SUPPLY → whole lockup (pulse + ring) | `a_fb` cues × `lock_amt` |

Frame table v1.1 (`F` in timeline.json): MTN 25/40/54 · DROP 68 · LAND 78 · BOX 135 · PEAK 141 · PET 168 · SETTLE 177 · WAVES 190, 213 · VOCAL 216→361, syllables 284 295 307 319 329 338 360 (the 7.20 one sits 1 f before the window opens) · FLASH 361 · LOCKS 366 375 402 410 · STILL 417.
