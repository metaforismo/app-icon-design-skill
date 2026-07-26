# Apple app-icon platform specifications

Current-source snapshot: 2026-07-26. Re-check Apple’s HIG and Xcode documentation before release work because platform tooling changes.

## Contents

- [Current platform matrix](#current-platform-matrix)
- [Masking and layout](#masking-and-layout)
- [Color and transparency](#color-and-transparency)
- [Icon Composer versus asset catalogs](#icon-composer-versus-asset-catalogs)
- [Legacy asset-catalog notes](#legacy-asset-catalog-notes)
- [Claims to avoid](#claims-to-avoid)

## Current platform matrix

Apple’s June 2026 HIG lists:

| Platform | Source layout | Final system mask | Layout size | Style | Appearances |
| --- | --- | --- | ---: | --- | --- |
| iOS, iPadOS, macOS | Square | Rounded rectangle | 1024 × 1024 px | Layered | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | 800 × 480 rectangle | Rounded rectangle | 800 × 480 px | Layered parallax | Not applicable |
| visionOS | Square | Circle | 1024 × 1024 px | Layered 3D | Not applicable |
| watchOS | Square | Circle | 1088 × 1088 px | Layered | Not applicable |

The system scales the icon for smaller system locations. Do not maintain a folklore size list when Xcode can show the current target’s exact wells and when Icon Composer can render the variants.

## Masking and layout

- Supply unmasked square or rectangular layers. Let the system apply the final rounded-rectangle or circular mask.
- Keep primary content centered and use the current Apple production grid. Do not substitute a made-up percentage safe zone for the official template.
- Avoid borders that depend on the final mask edge. Pre-masking can create jagged edges and weak specular highlights.
- Check circular platforms separately. A composition that feels centered in a rounded rectangle can look low or wide in a circle.
- Keep content bold enough for small locations. Avoid thin line weights and sharp corners that lose crispness.

## Color and transparency

Apple lists these supported color spaces:

- sRGB for color
- Gray Gamma 2.2 for grayscale
- Display P3 for wide-gamut color on iOS, iPadOS, macOS, tvOS, and watchOS

Use the delivery path to decide transparency:

- **Icon Composer layer sources:** transparency is normal because each SVG or PNG represents a layer.
- **Flattened legacy iOS App Store master:** use an opaque 1024 × 1024 image unless current Xcode documentation for the exact path says otherwise.
- **Asset-catalog dark/tinted variants:** follow the current Xcode instructions. Tinted is grayscale; dark can use transparency so the system background shows.

Do not generalize one path’s alpha rules to every source layer and platform.

## Icon Composer versus asset catalogs

Use Icon Composer as the production authoring route for a compatible shipping icon across iOS, iPadOS, macOS, watchOS, and the App Store. Use the `.icon` file that Icon Composer creates; do not call it `.iconset`, `.icns`, or an asset-catalog folder.

Use asset catalogs when:

- the target is tvOS or visionOS
- exact legacy artwork must remain on older releases
- a complex illustrative design cannot survive Composer translation and the user selects a flattened fallback
- the platform workflow explicitly requires an image stack or icon set

Adding an Icon Composer file to a target can replace the existing icon asset catalog for that app icon. Inspect target settings before editing.

## Legacy asset-catalog notes

Current Xcode can generate many iOS, iPadOS, tvOS, and watchOS variants from one high-resolution image. macOS and tvOS may still require individual size assets depending on the selected asset-catalog configuration.

iOS and iPadOS asset catalogs support Any, Dark, and Tinted image wells. When using alternate icons, configure the project’s alternate icon sets and verify the resulting `CFBundleIcons` entries through the supported Xcode workflow.

Do not manually invent `Contents.json` entries from memory for a live project. Let Xcode create the icon set, then place assets into the wells or make narrowly scoped edits to the generated manifest.

## Claims to avoid

- Do not promise App Review approval.
- Do not claim that a 1024 × 1024 PNG is the only valid source for every current platform.
- Do not claim that tvOS or visionOS use Icon Composer when Apple’s current docs keep them on asset catalogs.
- Do not claim all six iOS/macOS appearances are separate top-level authoring modes. Icon Composer exposes Default, Dark, and Mono; Clear and Tinted previews are options within Mono.
- Do not claim a fixed central 70% safe zone as Apple guidance unless the current official template explicitly provides it.
