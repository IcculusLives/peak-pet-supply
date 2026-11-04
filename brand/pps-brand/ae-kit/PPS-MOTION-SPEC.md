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

---
## v1.2 — Casey's re-tune baked (2026-10-18, royce-claude) — dog lands on the 808
Casey tuned in the offline Brand Lab (Chrome, 127.0.0.1:8790) and 📋-pasted; baked into `_build/gen_previz.py`, previz + `parts/timeline.json` regenerated.
Starts (s): bed 0.00 · **808 2.23** (hit 0.075 in → **2.31**) · **PPS 2.5 3.96** (hit → 4.13) · **jj 4.88** (hit → 5.05) · PPS 2 = VOCAL 5.89 · FB pearl 11.59 (unchanged). Gains unchanged.
Visual hits: **dog lands 2.42** (F 73, drop 63) · **box 4.07** (F 122) · **PEAK 4.99** (F 150) · PET SUPPLY 5.60 · settle 5.89 · flash 12.03 (now on the vocal's last note, 12.01 — no 808 under it any more; FB lock-ticks 12.19 / 12.50 / 13.39 / 13.68 follow) · still 13.90. Peaks, shockwaves, vocal window unchanged.
Note for the next pass: the landing squash (2.42) sits ~3 f after the 808 transient (2.31); v1.1 had the visual 2 f *ahead* of its hit. If it reads late, `land` 2.29 puts it back ahead. Status: **tuned, Casey has "a couple more teensy edits" before lock** — still no ExtendScript.
Previz pages now carry a 📥 paste-settings button (bottom-left) so a JSON from Claude can be tried in one paste; `_build/buddy-paste.html`, injected by gen_previz.py.

---
## v1.3 — Casey's three edits (2026-10-18 00:15, royce-claude) — kick removed, late syllables, THE BOA
All three are sliders (new panel sections) and baked as defaults in `_build/gen_previz.py`; previz + `parts/timeline.json` regenerated.
1. **Bed duck = kick removal.** The "kick right after the bass drop" is in the bed (PPS_1pearl): a lone 90 ms low hit at **2.49–2.58**, near-silence (≈ −40 dBFS) either side. The 808 file itself is one clean boom. Fix: bed gain → 0 over `duck_t 2.47` + `duck_len 0.14` (`duck_amt 1.0`). In the page it's a per-frame volume gate on the bed element; **in AE = two audio-level keyframe pairs on the bed layer** (F 74–78).
2. **Late syllable group.** `syl2_off −0.12 s` shifts every syllable burst after the held note (in-file ≥ 3.5 s) earlier; the first group is untouched (Casey: "before that is perfect"). SYL now 281 292 303 315 326 334 357 (was 284 295 307 319 329 338 360). Tune by ear.
3. **The boa.** When the FB pearl starts (`a_fb` + `boa_off 0` = 11.59, F 348) a pink, sparkly feather boa grows round the dog's neck, venom-style: two tendrils from the back of the neck wrap both ways and meet under the chin over `boa_grow 1.1 s`; the growing tips wriggle; once grown it breathes with the voice level and sways ±2.5° (1.7 s period); 4-point white sparkles twinkle on ~⅓ of the tufts and tiny motes float up. Neck ellipse (comp px, inside the dog layer so it squashes/swells with the dog): centre 1006,190 · rx 43 · ry 15 · tilt 24°. Pinks `#FF3D9A #FF6FB5 #FF8FC8 #FFB3DA #F0197F`, highlights `#FFD6EC`, sparkle white. Each tuft = core + 1.25× and 1.7× soft halos. Back half of the ellipse renders behind the dog (`#boaB`), front half + sparkles in front (`#boaF`). Sliders: `boa_off` `boa_grow` `boa_size 1.0` `boa_sparkle 1.0` `boa_amt 1.0` (0 = no boa). **AE:** one boa comp parented to the dog (anchor at the neck centre), tuft layers revealed along the arc with a trim-paths-style grow; sparkles = a small particle/shape set; not built until lock.
Status: **tuned, not locked** — Casey to play with the three new sections.
- **v1.3b (00:40) — boa tail.** Once the tendrils meet, a strand drops from the meeting point under the chin (`P(0)`), tapering to a pompom, with a 20 f overshoot drop; swings as a pendulum (1.3 s period, ±7°, lower end lags) on top of the collar sway; sparkles on a few tufts. `boa_tail` = length in comp px (default 140; 0 = none). Tufts every 8 px with the same halo stack as the collar. AE: a second shape group parented to the boa comp, pivot at the chin point.
- v1.3c (00:42): collar tufts set to the tail's gauge (core 10–15 px × size).

---
## v1.4 — Casey's 📋 "done" (2026-10-18 00:48) — LOCK CANDIDATE
Baked exactly as pasted. Changes from v1.3: **808 start 2.28** (hit 2.355; landing squash 2.42 = 2 f after the hit) · **boa grows over 1.95 s** · boa presence 0.8 · tail 115 px · **duck_t 0.00** (the bed duck now sits at 0.00–0.14 where the bed is silent — i.e. the 2.49 kick is NOT removed; flagged to Casey: intended, or slid by accident? `duck_t 2.47` restores the cut). Everything else as v1.3.
Frame table: MTN 25/40/54 · DROP 63 · LAND 73 · BOX 122 · PEAK 150 · PET 168 · SETTLE 177 · WAVES 190 213 · VOC 216→361 · SYL 281 292 303 315 326 334 357 · BOA 348 (grown by 407, tail drops ~398) · FLASH 361 · LOCKS 366 375 402 410 · STILL 417.
Status: **locked by Casey pending the duck answer → next step is the AE build (build-comp.jsx from parts/registration.json + timeline.json, CSD template)**.
- v1.4a (00:52): duck_t back to 2.47 — Casey had zeroed it only because the control wasn't clear; kick removal stands. v1.4 otherwise unchanged. **LOCKED.**

---
## AE build v1 written (2026-10-18 01:05, royce-claude cloud) — not yet run in AE
`ae-kit/build-comp.jsx` (ES3, CSD template; writes `build-log.txt`), `RUN-AE-BUILD.command` (DoScript runner, CSD pattern), `AE-BUILD-NOTES.md` (layer list, approximations, re-run after re-bake). Builds `PPS_Summit` + `PPS_Boa` precomp from the locked v1.4 F table, with the bed duck as audio-level keyframes. Run: `bash ~/code/peak-pet-supply/brand/pps-brand/ae-kit/RUN-AE-BUILD.command` with AE 2026 open. First run on pewter is the real test — expect a fix or two from `build-log.txt`.

## v1.5 — first AE build + Casey's directions (2026-10-20, royce-claude) — LOCKED, built, rendered from `ae-kit/PPS_Summit.aep`
Built in AE 2026 by `ae-kit/build-comp.jsx` (run with `zsh ae-kit/RUN-AE-BUILD.command`; stills `RUN-AE-SNAP.command`; render `RUN-AE-RENDER.command`). Changes on top of the v1.4 lock (ported back into `_build/gen_previz.py` the same evening — previz and AE agree; the previz stores its tune under `pps_summit_cfg15` so the old v1.4 tune no longer overrides the new defaults):
- **Length 14.9 s** (F 447): ~0.7 s of silence after the riff while the boa tail (and a ±2.5° collar sway) keep moving.
- **Jaw.** Off-white lower jaw hinged at the mouth corner (1042,158), hidden inside the muzzle when closed, swings down up to 40° on a per-frame `mouth` slider (VOICE null) = 250–3500 Hz RMS of the three vocal placements: PPS 2.5 @3.96 "honey I said", jj @4.88 (same stab), PPS 2 @5.89 (third "honey I said" → held "oh" → later syllables). Active F 120–355.
- **Howl arcs** (white) now cover all the singing from 3.96 s, level from the mouth envelope before 7.2 s; the howl window is capped 15 f early and the 11.9 s syllable burst is dropped so nothing is still fading after the last note (12.03). Gold syllable bursts unchanged (9.37 s on).
- **Boa v2** = tuft-for-tuft port of the previz (25 tufts per tendril, 1.7×/1.25×/1× halos, highlights, sparkles), split into `BOA back` (upper half, behind the dog) and `BOA front` (lower half + tail + sparkles) — both parented to the dog. Tail shortened to 78 px so the pompom hangs just above the summit. Grows continuously (ease-out) from the first riff hit (11.79) to the last (13.92); the collar pulses on every riff hit (spectral-flux onsets of PPS_FB_pearl: 11.79 12.11 12.42 12.71 13.03 13.33 13.61 13.92, strongest 12.71); tail drops on the 12.71 hit; sway starts once grown (14.2).
- **Dog tail wag** ±6° from the landing (2.42) on the bed's pulse (PPS_1pearl low-band autocorrelation 0.785 s ≈ 76 BPM, hits at 0.575 + k·0.785 s). Rig: subtract mask cuts the tail (crescent off the rump, pivot 826,308) out of the dog; a second dog copy masked to the tail (+6 px overlap under the body) is parented to the dog and rotates.
- **Mountains launch fast** (linear out of their first key) — the ease-in on the first AE build read as a late start vs the previz.
