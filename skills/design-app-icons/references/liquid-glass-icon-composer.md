# Liquid Glass and Icon Composer workflow

Current-source snapshot: 2026-07-23.

## Contents

- [What Icon Composer is](#what-icon-composer-is)
- [Prepare source artwork](#prepare-source-artwork)
- [Create and organize the icon](#create-and-organize-the-icon)
- [Apply material intentionally](#apply-material-intentionally)
- [Understand appearances](#understand-appearances)
- [Add the icon to Xcode](#add-the-icon-to-xcode)
- [Test and retain evidence](#test-and-retain-evidence)
- [Migration traps](#migration-traps)

## What Icon Composer is

Icon Composer creates a single multilayer `.icon` file for iPhone, iPad, Mac, Apple Watch, and App Store rendering. It can preview platforms, appearances, backgrounds, lighting, and scale, and can export a flattened image for marketing.

Apple’s 2026 refinement adds sharper material rendering, selectable refraction, updated specular highlights, shadows, and earlier-release previews. Treat these controls as current tooling, not as bitmap filters to imitate before import.

## Prepare source artwork

For a new icon or redesign, require `Approved — production authorized` and a completed `design-approval.yaml` before preparing sources. A Liquid Glass migration of already-approved owned artwork may treat that supplied artwork as the approved concept when the user explicitly requests production.

1. Start from the latest Apple Design Resources app-icon template.
2. Use 1024 × 1024 for iPhone, iPad, and Mac; use 1088 × 1088 for Apple Watch.
3. Draw back-to-front layers in a vector editor.
4. Separate only the graphics that need independent color, material, appearance, platform, or depth behavior.
5. Convert essential text to outlines because SVG does not preserve fonts.
6. Name exports numerically, such as `01-wave.svg`, `02-sun.svg`, and `03-accent.svg`.
7. Remove effects that Icon Composer should own: blur, shadow, specular, opacity, translucency, background color, and background gradient.
8. Prefer SVG. Use PNG for unsupported SVG features.
9. Export full unmasked layers; never export the final platform mask.

Do not force a complex illustration into many depth slices. Apple documents a maximum of four groups. Fewer groups are usually clearer.

## Create and organize the icon

Open the latest Xcode and choose **Xcode > Open Developer Tool > Icon Composer**, or use Apple’s standalone download.

Before opening Composer, recompose the exported SVG/PNG sources and compare the result with the approved concept. If metaphor, silhouette, composition, focal scale, or palette drifted materially, return to concept review and obtain re-approval.

1. Create and save a file with the intended Xcode app-icon name, commonly `AppIcon.icon`.
2. In the Document inspector, enable only the supported platforms to reduce accidental variations.
3. Drag SVG/PNG files or folders into the sidebar.
4. Organize layers into at most four groups. Sidebar order is back-to-front.
5. Keep layer and group names explicit.
6. Use the canvas grid and numeric x/y/scale controls for precise placement.
7. Use platform-specific composition overrides only when a unified layout fails a real crop or optical-centering check.

Keep source design files outside the `.icon` file too. The Icon Composer document is delivery metadata and material annotation, not a replacement for the editable vector source.

## Apply material intentionally

Use the Appearance inspector:

- **Color:** automatic, none, solid, gradient, and opacity
- **Liquid Glass:** blur/frostiness, translucency, specular highlights, refraction, shadows, and related current controls
- **Composition:** visibility, position, scale, platform variations

Material rules:

- Keep the recognition anchor opaque enough to survive clear and tinted contexts.
- Use translucency where seeing through the layer explains depth; do not use it merely because it is fashionable.
- Apply refraction selectively. Strong lens distortion can destroy a small silhouette.
- Prefer crisp inner or outer specular highlights that define geometry without doubling every edge.
- Use the lighting control to expose weak contrast, not to choose one flattering angle.
- Preview on bright, dark, saturated, and image wallpapers.
- Avoid busy textures under refractive glass.
- Do not reproduce glass by baking highlights and shadows into the source art unless a specific non-Icon-Composer fallback requires it.

## Understand appearances

Icon Composer’s main authoring choices are **Default**, **Dark**, and **Mono** for iOS/macOS. Mono options preview:

- light or dark
- clear or tinted
- a chosen tint color

Apple’s HIG describes the resulting supported iOS/iPadOS/macOS appearances as Default, dark, clear light, clear dark, tinted light, and tinted dark.

Keep the identity anchor consistent. Vary fill, opacity, material, or backdrop to protect legibility. Avoid redesigning the silhouette in each appearance because that weakens recognition.

Apple Watch has no appearance variants in Icon Composer. Test its circular mask and 1088 × 1088 layout separately.

## Add the icon to Xcode

1. Drag the `.icon` file into the Project navigator.
2. Select the target’s General pane.
3. Under **App Icons and Launch Screen**, set the App Icon field to the `.icon` filename without the extension.
4. Build for a simulator and device.
5. Inspect the compiled app rather than assuming the Project navigator preview proves delivery.

The latest Xcode uses the matching Icon Composer file instead of an existing `AppIcon` asset catalog. If the app supports earlier releases, Xcode can generate flattened icons at build time. If the exact historical icon must remain, continue using asset catalogs rather than accepting an automatically similar fallback.

## Test and retain evidence

Capture:

- Icon Composer screenshots for each platform and appearance
- at least one challenging bright and one challenging dark wallpaper
- small-size previews
- Xcode target setting
- successful build output
- Simulator Home Screen or Dock placement
- a physical device when release risk justifies it
- older-release preview or device evidence when minimum deployments matter

Separate static, Simulator, and device evidence. A static exported PNG cannot prove dynamic specular, refraction, masking, or gyro behavior.

## Migration traps

- Naming a file `AppIcon.icns` or `AppIcon.iconset` instead of using Icon Composer’s `.icon` file
- Keeping baked shadows, blur, highlights, gradients, and mask corners in imported source art
- Using more than four depth groups
- Treating every transparent shape as glass
- Assuming a flat concept image can be imported and remain independently editable
- Forgetting that tvOS and visionOS remain asset-catalog workflows
- Replacing the existing asset catalog before comparing earlier-release output
- Calling the result “Liquid Glass validated” without an Icon Composer or runtime preview
