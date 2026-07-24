# Mood Lantern

![Mood Lantern concept](concept-master.png)

The [layer-first experiment](layer-first/README.md) also demonstrates one-element-per-generation assembly and records the baked-checkerboard transparency failure honestly.

## Brief

- Fictional product: emotion journal
- Promise: notice and reflect on feelings
- Direction: expressive mascot
- Recognition anchor: lantern body with one warm core

## Why it works

The silhouette communicates “lantern” without a second prop. Large eyes and a small mouth establish calm curiosity, and the core glow ties the character to reflection and inner state.

## Risks

- The face can drift toward generic emoji grammar.
- The handle, cap, rings, eyes, mouth, body, and light create too many literal parts.
- The warm light occupies a large area and can erase the body in clear or tinted appearances.
- The body’s shading is too continuous to import as editable vector layers.

## Production reconstruction

Use four groups:

1. background fill in Icon Composer
2. unified lantern silhouette including handle and base
3. face as a single opaque group
4. core window as a restrained translucent group

Remove one ring, reduce eye highlights, flatten the face, and keep the core smaller. Test whether the silhouette remains recognizable without the face.

## Status

- **Validated:** original concept dimensions; actual alpha inspection of separated outputs; reproducible chroma cleanup and composite; static iOS audit of the assembled proof.
- **Prepared:** generated concept, prompts, alpha-normalized raster candidates, and assembled proof; current candidates are not approved for import.
- **Not tested:** Icon Composer import, Xcode, Simulator, device, App Store, or conversion.
