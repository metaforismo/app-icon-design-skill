# Research notes

Last checked: 2026-07-26.

## Current Apple baseline

The repository follows Apple’s June 2026 HIG update and current Icon Composer documentation:

- iOS, iPadOS, and macOS use 1024 × 1024 square layered sources with rounded-rectangle system masks.
- watchOS uses a 1088 × 1088 square source and a circular system mask.
- tvOS uses an 800 × 480 layered parallax asset-catalog workflow.
- visionOS uses a 1024 × 1024 layered 3D asset-catalog workflow and a circular mask.
- Icon Composer creates a `.icon` file for iPhone, iPad, Mac, Apple Watch, and App Store use.
- Current Icon Composer guidance limits a document to four depth groups.
- Icon Composer exposes Default, Dark, and Mono authoring modes; Clear and Tinted light/dark are Mono previews.
- 2026 tooling includes refined material rendering, refraction, specular controls, and earlier-release previews.
- The object model distinguishes imported graphic layers from at most four rendered depth groups. Groups can render their layers individually or as one combined glass object.
- The icon canvas owns simple background fills; group controls own shared material; layer controls own image, color, composition, and whether Effects are enabled.
- Current Xcode selects the `.icon` whose filename matches the target’s App Icon setting and generates earlier-release images when applicable.

## Local tool observation

The v2 workflow was checked against macOS 26.5.2, Xcode 26.6 (17F113), and bundled Icon Composer 1.6 (99.1). The existing Quiet Tide `.icon` fixture was rebuilt successfully for a generic iOS Simulator destination on 2026-07-26. Its earlier Composer captures and Simulator Home Screen evidence remain the directly observed runtime example. This does not validate new artwork, physical-device material response, or every Xcode fallback.

## Corrections to secondary material

The supplied MobileAction article was useful for workflow ideas but included claims that were outdated, imprecise, or unsupported as current Apple facts:

| Claim | Current handling |
| --- | --- |
| Use a Liquid Glass `.iconset` | Icon Composer creates `.icon`. |
| Keep content inside a fixed central 70% | Use Apple’s current production grid; the HIG does not establish a universal 70% rule. |
| Use Default Light/Dark as separate modes | Icon Composer exposes Default, Dark, and Mono; the HIG lists six resulting appearances. |
| A 14-day test is required | Apple recommends waiting for evidence and reports confidence; no universal 14-day minimum is documented. |
| A refreshed icon improves ranking | Treat this as an unverified marketing hypothesis; measure conversion rather than asserting causation. |
| Following HIG ensures review approval | No design checklist guarantees App Review approval. |

## Reference-set analysis

The 61 user-supplied examples were studied as a private inspiration corpus. They broadly demonstrate:

- tactile utility objects
- minimal geometric symbols
- bold flat emblems
- friendly mascots
- dark chrome and metal
- translucent layered glass
- physical-device miniatures
- abstract gradient ribbons

The repository retains only this generalized taxonomy. It does not copy, trace, embed, name, or redistribute the third-party icons.

## Evidence boundary

The bundled examples prove:

- the built-in image-generation workflow can produce original, coherent, square concept masters
- prompts can constrain output to one metaphor, strong small-size hierarchy, and a plausible layer plan
- the static validator can inspect 1024 × 1024 files and create preview sheets
- the Quiet Tide example can be reconstructed into deliberate SVG sources, saved in Icon Composer, compiled by Xcode, and observed in one Simulator context

They do not prove:

- automatic editable reconstruction for every generated visual
- Composer compatibility for every generated visual
- physical-device rendering or gyro response
- App Store acceptance
- conversion or ranking lift
