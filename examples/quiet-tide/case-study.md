# Quiet Tide

![Quiet Tide concept](concept-master.png)

## Brief

- Fictional product: calm-focus app
- Promise: make focused work feel steady
- Direction: layered abstract identity
- Recognition anchor: one aqua wave embracing one coral sun

## Why it works

The concept reduces “calm focus” to two masses. The wave provides movement without a thin orbital line; the sun supplies a small warm focal point. The deep field keeps the translucent shape readable.

## Risks

- The curl may collide with generic wave or wellness marks.
- Strong internal shading makes the bitmap more illustrative than a production vector.
- The wave and lower bowl merge at very small sizes.
- The concept’s glass effect is baked into the bitmap and does not prove Icon Composer behavior.

## Production reconstruction

Use three groups:

1. background fill in Icon Composer
2. wave silhouette as one clean SVG group
3. sun disc as an opaque SVG group

Redraw the wave with fewer control points, reduce the lower bowl, keep the sun fully separated, and let Icon Composer own specular, refraction, shadow, and translucency.

## Status

- Validated: static concept audit; intentional SVG reconstruction; Icon Composer import and appearance previews; Xcode simulator build; iOS 26.5 Simulator install, launch, and Home Screen icon
- Prepared: generated concept, full prompt, editable SVGs, real `QuietTide.icon`, reproducible XcodeGen fixture, and evidence ledger
- Not tested: physical device, signed archive, App Store upload/review, Product Page Optimization, ranking, or conversion

See the [production reconstruction](production/README.md) and [evidence ledger](production/evidence.md).
