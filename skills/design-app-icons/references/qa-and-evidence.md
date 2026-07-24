# App-icon QA and evidence

## Contents

- [Evidence levels](#evidence-levels)
- [Static preflight](#static-preflight)
- [Small-size review](#small-size-review)
- [Mask and appearance review](#mask-and-appearance-review)
- [Xcode and runtime review](#xcode-and-runtime-review)
- [Accessibility and inclusion](#accessibility-and-inclusion)
- [Report format](#report-format)

## Evidence levels

Use explicit labels:

1. **Concept inspected:** generated or drawn image reviewed at full size.
2. **Static preflight passed:** dimensions, mode, alpha, and small previews checked.
3. **Icon Composer previewed:** platforms, appearances, material, and masks observed.
4. **Xcode build validated:** target setting and successful build observed.
5. **Simulator validated:** icon observed in system context.
6. **Device validated:** icon observed on named hardware and OS.
7. **Store validated:** uploaded/approved product-page asset observed.
8. **Experiment measured:** Product Page Optimization result observed with uncertainty.

Never collapse these levels into “done.”

## Static preflight

For a flattened iOS master:

- exact 1024 × 1024 pixels
- supported RGB or grayscale color space
- opaque corners and no accidental alpha
- no baked system mask
- no outer mockup background
- no watermark, fake text, or third-party mark
- focal content inside the official current grid

For a layer source:

- full canvas dimensions
- transparency where no art exists
- clean antialiasing
- no background plate unless the design requires an independently rendered shape
- no baked blur, shadow, specular, or refraction intended for Icon Composer
- meaningful filename and z-order

Use `scripts/icon_qa.py` for repeatable dimension/alpha checks and previews.

## Small-size review

Inspect nearest-neighbor-free downscales at:

- 16, 20, 29, 40, 60, 76, 83, 128, and 256 px for a broad iOS/macOS audit
- additional current Xcode sizes for the specific target

Ask:

- Can a person describe the symbol in one short phrase?
- Does the focal point remain first?
- Do adjacent masses merge?
- Does a highlight disappear and change the perceived shape?
- Does text become noise?
- Does the icon still differ from category neighbors?

Do not judge only on a zoomed 1024-pixel canvas.

## Mask and appearance review

Use the current Apple production grid and Icon Composer:

- rounded rectangle for iOS/iPadOS/macOS
- circle for watchOS
- circle for visionOS asset-catalog work
- tvOS safe zone and parallax crop

For iOS/macOS, test Default, Dark, and Mono authoring states plus clear/tinted light/dark previews. Use multiple wallpaper types and move the lighting control.

Log any platform override. If a platform requires a different scale or position, preserve the same recognition anchor.

## Xcode and runtime review

1. Confirm the intended `.icon` filename or asset-catalog source in target settings.
2. Build with the current scheme.
3. Inspect compile warnings and asset errors.
4. Observe the icon in relevant system surfaces: Home Screen, Spotlight/search, Settings, notifications, App Library, Dock, or Watch app list as applicable.
5. Test older supported releases when fallback rendering matters.
6. Capture settled screenshots after each appearance change.
7. Record device, OS, Xcode, and Icon Composer versions.

Static exports do not prove dynamic material. Simulator evidence does not prove a physical display or gyro response.

## Accessibility and inclusion

App icons do not expose a separate accessible label inside the artwork; the app name and system context carry semantics. Therefore:

- avoid relying on icon text for meaning
- do not rely on color alone to distinguish the main symbol
- keep shape contrast strong in grayscale and tinted modes
- avoid culturally ambiguous or stigmatizing metaphors
- check whether a hand gesture, face, flag, letter, or animal changes meaning across target markets
- verify that essential text or initials survive localization strategy

Do not claim a WCAG contrast pass for an icon unless a specific measurable criterion and context is documented. Use contrast measurements as a heuristic.

## Report format

```markdown
## Status

- Validated:
- Prepared:
- Not tested:

## Artifact

- Source:
- Dimensions:
- Color mode:
- Alpha:
- Platforms:

## Visual findings

1. [P0-P3] Finding — evidence — consequence — recommendation

## Platform matrix

| Platform | Appearance | Static | Composer | Simulator | Device |
| --- | --- | --- | --- | --- | --- |

## Risks

- Similarity:
- Small-size:
- Mask:
- Material:
- Delivery:

## Evidence

- command/log:
- screenshot:
- version:
```

