# Layer prompts and provenance

All calls used the built-in `image_gen` tool on 2026-07-24 and referenced the original Mood Lantern concept master. The concept is original and fictional.

## 01 — backdrop

Generate only the edge-to-edge deep-plum radial background, with no lantern or other object.

## 02 — lantern shell

Generate only the complete lantern shell and hardware at the final position, with the amber window removed and transparent. The requested alpha was not delivered; the visible checkerboard was baked into an RGB PNG.

## 03 — amber glow

Generate only the warm belly-light disk at the final position. The requested alpha was not delivered and placement drifted.

## Key-color retries

The shell and glow were edited separately to replace every background pixel with flat `#00FF00`. Those outputs are inputs to deterministic chroma cleanup, not final assets.

Rights note: original generated outputs. No user-supplied or third-party screenshots are redistributed.
