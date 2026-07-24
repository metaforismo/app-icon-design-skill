# Quiet Tide teaching reconstruction

This small SVG pack demonstrates how to translate a generated concept into intentional, unmasked geometry:

```text
01-backdrop.svg
02-sun.svg
03-wave.svg
```

The files are full 1024 × 1024 canvases with transparent unused space. They intentionally omit the generated bitmap’s blur, outer shadow, baked specular highlights, and continuous glass shading.

In Icon Composer:

1. Import the three numbered layers in back-to-front order.
2. Keep `01-backdrop.svg` opaque and full-canvas; it has no baked system mask.
3. Keep the sun mostly opaque.
4. Apply restrained translucency and refraction to the wave.
5. Preview Default, Dark, and Mono plus clear/tinted options.
6. Refine the curves and optical centering in the original vector editor.

This pack is a teaching approximation, not a shipped `.icon` file and not a traced reproduction of the generated pixels.
