# Research notes

Last checked: 2026-07-23.

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

The four bundled examples prove:

- the built-in image-generation workflow can produce original, coherent, square concept masters
- prompts can constrain the output to one metaphor, strong small-size hierarchy, and a plausible layer plan
- the static validator can inspect 1024 × 1024 files and create preview sheets

They do not prove:

- an editable vector reconstruction
- Icon Composer import or material behavior
- a valid `.icon` file
- Xcode build integration
- Simulator or real-device rendering
- App Store acceptance
- conversion or ranking lift

