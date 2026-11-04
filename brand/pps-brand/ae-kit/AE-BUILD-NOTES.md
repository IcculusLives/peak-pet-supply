# PPS "Summit" — After Effects build notes (v1, 2026-10-18, royce-claude)

Built from the **LOCKED previz v1.4** (`PPS-MOTION-SPEC.md` v1.4/v1.4a; `parts/timeline.json` F table). **Not yet run in After Effects** — written and syntax-checked in the cloud session; the first run on pewter is the real test. Expect the usual first-run fixes (a match name, an ease) — `build-log.txt` says how far it got.

## Run it
Open After Effects 2026 (new or any project), then in Terminal:
```
zsh ~/code/peak-pet-supply/brand/pps-brand/ae-kit/RUN-AE-BUILD.command
```
To build into a named project (opened first, saved after): `zsh …/RUN-AE-BUILD.command "$HOME/code/peak-pet-supply/brand/pps-brand/ae-kit/PPS_Summit.aep"`.
Or in AE: File › Scripts › Run Script File › `build-comp.jsx`. Prerequisite: Settings › Scripting & Expressions › **Allow Scripts to Write Files and Access Network** (the log + status files).
After a re-bake (`_build/gen_previz.py`), copy the new F table from `parts/timeline.json` into `var T={…}` at the top of `build-comp.jsx` (and `AUDIO` starts/gains, `BOA_GROW`), delete the "PPS — Summit" folder in the project, rerun.

## What it builds — comp `PPS_Summit` 1920×1080 · 30 fps · 435 f, folder "PPS — Summit" (parts/ + audio/ subfolders)
Top → bottom:
- `flash-white` — radial solid, 55 % → 0 over 20 f from F 361.
- `ring-*` (17) — shape-layer stroked ellipses expanding + thinning + fading: land white/gold (73/76), waves ×2 (190, 213 + gold +3), box (122), PEAK (150), settle (177), flash white/gold (361/365), lock ticks box/PEAK/PET-SUPPLY/lockup (366/375/402/410).
- `syllable-bursts` — 21 arc groups (3 per syllable at 281 292 303 315 326 334 357; white/gold/white), `howl-arcs` — one arc group every 5 f inside 216–361 where the voice level ≥ 0.12, sized by the level. Arcs = ellipse + Trim Paths 11.1–28.9 % (the 64° window around −18°).
- `aura-gold` — Add-blend radial at the snout, opacity 45·lv², scale 100 + 55·lv.
- `LOCKUP-RIG` (null @ 960,540) — settle pulse +3 % (177), flash pulse +4.5 % (361), last lock tick +3 % (410); expression: breathe ±0.4 % at 2.4 s + 1.2 %·lv between F 189 and 361.
  - `box-gold` (anchor 960,769.1): pop 0 → 122 → 100 % (122/126/131), tick +4 % (366), +2 %·syl.
  - `PEAK` (967.3,704.8): pop 0 → 130 → 100 % (150/155/161), opacity in 3 f, tick +6 % (375), +7 %·syl.
  - `PET-SUPPLY` (963.3,866.5): rect mask wipe left→right 168–178, tick +6 % (402).
  - `EMBLEM-RIG` (null @ summit x, ground y 545.9): thud 103.5 % / 95 % (73–87), wave thuds (190, 213).
    - `BOA (PPS_Boa)` precomp layer — parented to `dog`, anchor 1006,190, 80 % opacity, scale 1 + 0.06·lv, rotation 2.5°·sin(2πt/1.7) once grown.
    - `dog` (anchor at the paws 915.7,398.1): opacity in at 63, falls 760 px 63 → 73 (ease-in), scale 96×106 in flight, squash 116×84 (76), 95×105 (80), 100 (83); expression swell 1.5 %/4.5 %·lv + 3 %·syl.
    - `dust-L/R` — off-white ellipses sliding out from the paws 73–91.
    - `mountain-left/center/right` (anchors on the ground line): scale-Y 0 → 105 → 100 over 25/40/54 +10/+16.
- `VOICE` (hidden null) — Slider `level` keyed every 3 f from the PPS_2 envelope (0..1), Slider `syl` = 1 → 0 over 9 f at each syllable. Every vocal expression reads these two.
- `thud-gold` — gold radial blink: 35 % on landing, 15 % on each wave, + 17.5 %·syl.
- `wash-blue` — 0 → 14 % over 40 f. `bg-navy`.
- `audio-bed / k808 / fb / two5 / p2 / jj` — starts 0.00 / 2.28 / 11.59 / 3.96 / 5.89 / 4.88; levels −4.4 / −0.7 / −1.9 / −3.1 / −5.2 / −1.9 dB (= the gains). **Bed duck:** audio levels −4.4 → −96 dB at F 73→74, back at 78→79 — removes the bed's kick at 2.49 s.

### `PPS_Boa` precomp
Dotted strokes (dash 0 + round caps = tufts) on the neck ellipse (86 × 30 px, rotated 24°) at 1006,190: 3 colour passes (pinks 1/3/5, dash offsets staggered) × 3 gauges — core 24 px @ 95 %, 1.25× halo @ 45 %, 1.7× halo @ 22 % — plus a lighter highlight pass. Trim Paths **Offset 90** puts the back of the neck at 50 %; Start 50 → 0 and End 50 → 100 over F 348 → 407 (1.95 s) reveal both tendrils from the back round to the chin. Wiggle Paths (size 6 → 0) on the core passes = the tips wriggle while growing. Tail: the same dotted stack on a 115 px vertical path from the chin point (1045.3, 207.5), Trim End 0 → 100 over 20 f from F 397 with a 112 % overshoot; group rotation expression = 7°·sin(2πt/1.3 + 0.8) + 4°·sin(2πt/1.7) once grown; `tail-pompom` (40 px) follows the tail end by expression. Sparkles: 6 four-point stars on the collar (each appears when its arc segment is revealed) + 2 on the tail, opacity = sin⁴ twinkle.

## Approximations vs the previz (tune in AE after the first build)
- **Boa z-order:** the previz draws the back half of the collar behind the dog and the front half in front; here the whole precomp sits in front of the dog. The collar reads fine on the silhouette; if the back half should tuck behind the head, duplicate `BOA (PPS_Boa)` below `dog` and mask the halves.
- **Trim Offset sign:** if the boa grows from under the chin instead of from the back of the neck, change `Trim Offset` 90 → −90 on every `collar-*` layer (one line in `boaDots`).
- Previz tufts had per-tuft random radii; the dotted stroke gives uniform tufts per pass — the three passes at different widths/offsets approximate the variation. Floating "motes" drifting up from the boa are not built.
- Howl arcs: previz spawns continuously and sizes each arc by the live level; here they're pre-sampled every 5 f (same as the previz's `voc_rate`). Ring/arc expansion uses bezier eases (75 % influence) instead of the previz's cubic ease-out — close.
- The vocal `level` slider is sampled every 3 f (0.1 s = the analysis resolution), linear between.
- Gold "thud" + blue wash are feathered-mask solids rather than true radial gradients.
- Dog fall: two position keys with 0.1 % / 90 % influence ≈ cubic ease-in.

## Then
`ae-render.sh` from the CSD kit works unchanged with `--comp PPS_Summit` (copy it here when rendering): QuickTime Animation master → H.264 via Media Encoder. Renders go to `renders/` (git-ignored).

## 2026-10-20 — first real build (v1.5)
- Runners are **zsh** (`${0:A:h}`): `zsh …/RUN-AE-BUILD.command` → `RUN-AE-SNAP.command` (saves `PPS_Summit.aep` + 27 PNG stills to `renders/stills/`) → `RUN-AE-RENDER.command` (render queue → `renders/PPS_Summit_pearl_v1.4.mp4`, H.264 template if AE has one, else ProRes/Lossless .mov).
- AE needs Settings › Scripting & Expressions › "Allow Scripts to Write Files and Access Network" (set on pewter 2026-10-20).
- Gotchas hit: (1) a second `fx()` on the same layer invalidates the first effect's slider reference — re-fetch by name; (2) `addShape()` layers sit at comp centre — zero anchor+position when group transforms carry comp coords; (3) runner catch must not concatenate the raw Error object (ExtendScript throws "Object of type Error found where…"); (4) the build removes any previous "PPS — Summit" folder first, so reruns don't pile up.
- See PPS-MOTION-SPEC.md v1.5 for what changed vs the previz lock.
