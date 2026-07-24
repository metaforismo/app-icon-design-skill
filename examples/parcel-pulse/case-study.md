# Parcel Pulse

![Parcel Pulse concept](concept-master.png)

## Brief

- Fictional product: parcel tracker
- Promise: see a package’s progress quickly
- Direction: tactile utility object
- Recognition anchor: one parcel crossed by one scan band

## Why it works

The physical parcel is immediately legible, while the electric band communicates an active scan without tiny barcode lines or a shipping label. The orange/cyan contrast separates object and action.

## Risks

- The tape seam and serrated edge are unnecessary at small sizes.
- The perspective and paper texture need simplification for SVG reconstruction.
- The scan band is luminous in the bitmap and may become too dominant in tinted modes.
- The rendered floor shadow is concept polish, not source-layer material.

## Production reconstruction

Use three or four groups:

1. background fill in Icon Composer
2. simplified parcel body
3. optional tape strip merged with the body when it does not need independent appearance control
4. scan band as the only translucent glass group

Use a flatter front-biased perspective and remove the serrated tape detail. Keep the cyan band readable without bloom.

## Status

- Prepared: generated 1024 × 1024 concept and full prompt
- Validated: static dimensions and alpha are covered by repository validation
- Not tested: vector reconstruction, Icon Composer, Xcode, Simulator, device, App Store, or conversion

