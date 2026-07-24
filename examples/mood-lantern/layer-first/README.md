# Mood Lantern: layer-first Imagegen experiment

This example tests the workflow in which Imagegen creates one visual role per image and the parts are assembled later.

## Composition contract

- Canvas: 1024 by 1024
- Camera: front-facing, orthographic-like product view
- Light: soft upper-left studio light plus a warm internal glow
- Palette: deep plum, lilac, amber, near-black
- Order: backdrop → glow → lantern shell
- Target boxes: shell `240,64,784,946`; glow `342,573,681,842`

## What happened

The first shell and glow generations looked transparent because they displayed a checkerboard. Static inspection proved that both were opaque RGB PNGs with the checkerboard baked into the pixels. Those files remain under `raw/` as explicitly rejected evidence.

The elements were regenerated on a uniform chroma-green background. `prepare_raster_layer.py` converts that key to alpha and re-establishes the recorded target box. The outputs are named `candidate/`, not `clean/`, because normalization does not approve their edges or geometry. This makes a useful assembly proof, but it does not eliminate every possible spill or prove Icon Composer quality.

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
- **Prepared:** alpha-normalized raster candidates and an assembled proof for design review. Visible fringe and aperture-seam mismatch keep them out of production.
- **Not tested:** Icon Composer import, Default/Dark/Mono authoring, Xcode build, Simulator, physical device, App Review, or conversion performance for Mood Lantern.

Inspect candidates at 100–400% over black, white, gray, and saturated backgrounds. The retained proof still shows colored fringe and an imperfect shell/glow seam, so the current candidates are rejected for Icon Composer import. For an identity whose silhouette must remain mathematically stable, reconstruct the shell as SVG and keep only a manually matted or regenerated glow as a raster layer.
