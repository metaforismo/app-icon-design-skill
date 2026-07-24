# Mood Lantern: layer-first Imagegen experiment

This example is a negative test of the workflow in which Imagegen creates one visual role per image and the parts are assembled later. The mechanics are reproducible; the visual result is rejected.

## Composition contract

- Canvas: 1024 by 1024
- Camera: front-facing, orthographic-like product view
- Light: soft upper-left studio light plus a warm internal glow
- Palette: deep plum, lilac, amber, near-black
- Order: backdrop → glow → lantern shell
- Target boxes: shell `240,64,784,946`; glow `342,573,681,842`

## What happened

The first shell and glow generations looked transparent because they displayed a checkerboard. Static inspection proved that both were opaque RGB PNGs with the checkerboard baked into the pixels. Those files remain under `raw/` as explicitly rejected evidence.

The elements were regenerated on a uniform chroma-green background. `prepare_raster_layer.py` converts that key to alpha and re-establishes the recorded target box. The outputs are named `candidate/`, not `clean/`, because normalization does not approve their edges or geometry. This makes a useful mechanical assembly proof, but the proof is visibly worse than the original concept and is not a production candidate.

## Why the decomposition failed

The original whole image uses one continuous rendering system: the amber core illuminates the lilac shell, softens the aperture boundary, and affects the character’s face and body. Independent generation broke that relationship:

- the warm core became a detached circular disk with a hard dark ring;
- the body became narrower and the cap, handle, base, and trim became heavier;
- face placement and spacing changed;
- shared reflected light and soft material transitions disappeared;
- the result feels assembled from parts instead of naturally illuminated.

The correct decision is to keep the original whole image as the final artwork. More layer repair would add time while moving farther from the approved design. A new vector-native or Composer-native interpretation would require a new concept and explicit approval.

## Reproduce the candidates and proof

Run these commands from the installable skill directory, adjusting paths to the example checkout:

```bash
python3 scripts/prepare_raster_layer.py raw/02-lantern-shell-key.png candidate/03-lantern-shell.png \
  --key-color 0,255,0 --threshold 170 --fit-box 240,64,784,946 \
  --report qa/shell-cleanup.json

python3 scripts/prepare_raster_layer.py raw/03-amber-glow-key.png candidate/02-amber-glow.png \
  --key-color 0,255,0 --threshold 170 --fit-box 342,573,681,842 \
  --report qa/glow-cleanup.json

python3 scripts/compose_raster_layers.py \
  candidate/01-backdrop.png candidate/02-amber-glow.png candidate/03-lantern-shell.png \
  --output assembled-proof.png
```

## Status

- **Validated:** the three raw generations exist; the supposed transparent outputs have no alpha; the key-color cleanup produces real RGBA candidates; the 1024 px flattened composite can be reproduced locally and has a retained static audit.
- **Prepared:** alpha-normalized raster candidates and a rejected assembled proof retained for teaching. Fidelity drift, visible fringe, and aperture-seam mismatch keep them out of production.
- **Not tested:** Icon Composer import, Default/Dark/Mono authoring, Xcode build, Simulator, physical device, App Review, or conversion performance for Mood Lantern.

Inspect candidates at 100–400% over black, white, gray, and saturated backgrounds. The retained proof still shows colored fringe, an imperfect shell/glow seam, and substantial design drift, so the current candidates are rejected for Icon Composer import. Do not infer that SVG reconstruction would automatically restore the original integrated glow; use the whole image unless the user approves a deliberately simplified reinterpretation.
