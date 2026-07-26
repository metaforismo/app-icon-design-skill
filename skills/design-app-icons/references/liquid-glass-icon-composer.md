# Icon Composer production workflow

Current-source snapshot: 2026-07-26. This reference follows Apple’s June 2026 HIG refinement, current Icon Composer documentation, and the behavior observed in Icon Composer 1.6 bundled with Xcode 26.6 on macOS 26.5.2. Recheck official documentation when the tool version changes.

## Contents

- [What the file represents](#what-the-file-represents)
- [Source-art contract](#source-art-contract)
- [The Composer object model](#the-composer-object-model)
- [Material controls](#material-controls)
- [Appearances and platform overrides](#appearances-and-platform-overrides)
- [Practical authoring sequence](#practical-authoring-sequence)
- [Xcode delivery and fallback behavior](#xcode-delivery-and-fallback-behavior)
- [Validation matrix](#validation-matrix)
- [Failure modes](#failure-modes)

## What the file represents

Icon Composer creates one Apple-authored multilayer `.icon` document for iPhone, iPad, Mac, Apple Watch, and the App Store. The system renders sizes, supported platforms, appearances, and dynamic Liquid Glass behavior from this document. Icon Composer can also export flattened artwork for marketing.

Use Icon Composer for a shipping icon on these supported platforms when the approved design can be represented faithfully. Use Xcode asset catalogs for tvOS and visionOS. For complex illustrative art that cannot survive separation, Apple still permits flattened image delivery; report that route honestly instead of forcing an inferior Composer translation.

Treat `.icon` as a tool-owned format. Create and save it with Icon Composer. Do not manufacture `icon.json`, copy a sample package, or rename a directory and call it valid.

## Source-art contract

Before opening Composer, require a named approved image and a reconstructed proof that matches it at 1024 px and 32 px.

Prepare artwork in a vector or raster editor:

- 1024 × 1024 canvas for iPhone, iPad, and Mac;
- 1088 × 1088 canvas for Apple Watch;
- current Apple production grid from Apple Design Resources;
- square, unmasked, full-canvas exports;
- SVG whenever the geometry can be expressed faithfully;
- PNG for raster texture, mesh gradients, or unsupported SVG features;
- converted text outlines where essential;
- numbered, meaningful filenames from back to front.

Keep the source deliberately plain. Remove:

- rounded-rectangle or circular canvas masks;
- background colors and simple gradients that Composer can own;
- baked drop shadows between depth groups;
- bevels, edge specular, refraction, blur, and platform-material translucency;
- accidental presentation backgrounds and outer tile shadows.

Retain intrinsic artwork such as intentional grain, painted shading, or a raster texture only when removing it would change the approved identity.

## The Composer object model

Understand the hierarchy before tuning:

| Level | Purpose | Typical controls |
| --- | --- | --- |
| Document | Supported platform scope | iOS only/shared iOS–macOS choice, watchOS on/off |
| Icon canvas | System-owned background | solid or gradient fill |
| Group | One rendered z-depth plane | order, Individual/Combined material mode, specular, refraction, blur, translucency, shadow |
| Layer | One imported graphic inside a group | image, fill, opacity, blend, visibility, position, scale, Effects on/off |

Use a maximum of four groups. Groups—not every imported graphic—become the rendered depth planes. A group can contain multiple layers so related color pieces can share z-depth while retaining separate appearance fills.

Choose group mode intentionally:

- **Individual:** each layer receives its own material boundary and highlight. Use for distinct shapes that should read as separate pieces of glass.
- **Combined:** the group is treated as one composite object. Use when adjacent or overlapping layers form one silhouette and internal seams must not become separate glass edges.

Start with fewer groups. Add depth only when it improves recognition, occlusion, or material response. Do not allocate a group to every highlight or decorative detail.

## Material controls

Composer automatically applies Liquid Glass when graphics are imported. Tune the effect at the group level and disable it on layers that must remain flat or opaque.

### Specular

Specular creates the dynamic edge highlight and slight background response that define the glass boundary. Keep it enabled by default. Current controls can determine whether highlights align inside, outside, or automatically according to layer color. Inspect several lighting angles; a good still frame can hide a broken edge response.

Disable or reduce specular when:

- a flat opaque brand element must not look hollow;
- nested edges produce noisy double highlights;
- a thin form loses contrast;
- the approved design depends on a quiet matte surface.

### Refraction

Refraction bends color and shape from content behind the group. Use low strength for subtle edge presence and higher strength only for a deliberate lens-like focal element. Excess refraction can deform the recognition anchor, merge nearby shapes, or make Clear/Tinted variants illegible.

Test refraction over multiple backgrounds; a setting that looks good over one color may become muddy or distracting over a detailed wallpaper.

### Blur and translucency

Blur softens what transmits through the material; translucency controls how much underlying color and form remain perceptible. Use them together, not as independent decoration. Preserve at least one opaque or high-contrast recognition anchor so the icon survives Clear and Tinted modes.

### Shadow

Shadow separates rendered groups in z-depth. Use enough to clarify order at small sizes, not enough to recreate a static floating-object illustration. Check dark appearance, where neutral shadows can disappear or become too heavy.

### Color and opacity

Use icon, group, or layer fills to create controlled Default, Dark, and Mono variants. Composer supports automatic source color, none, solid, and gradient fills. Vary appearance color before changing geometry. Avoid making every variant a different identity.

## Appearances and platform overrides

Composer authors three modes:

- **Default**
- **Dark**
- **Mono**

From Mono options, preview:

- Clear light
- Clear dark
- Tinted light
- Tinted dark

These previews are not four additional independent icon structures. Keep the same recognition anchor and core elements in every mode. For Mono, establish a clear luminance hierarchy: at least one light anchor, distinct gray roles, and sufficient separation after tint infusion.

Use the inspector’s `All` view to audit every overridden value. Add appearance variation under Color or Liquid Glass only when needed. Add platform variation under Composition for optical scale or position—not to introduce a different symbol.

For watchOS, inspect the circular crop and 1088 grid. There are no watchOS appearance modes in Composer. A shared vector design can use a platform-specific scale or position, but essential raster sources may need separately reviewed exports.

## Practical authoring sequence

1. Launch **Xcode → Open Developer Tool → Icon Composer**.
2. Create and save a named `.icon` document before importing.
3. In the Document inspector, hide unsupported platforms.
4. Set the canvas background to a solid or soft gradient when possible.
5. Import numbered SVG/PNG files or folders. Verify alphabetical order and actual z-order.
6. Organize graphics into no more than four semantic depth groups.
7. Decide Individual versus Combined for every multi-layer group.
8. Check the unmodified Default result before tuning; this establishes the automatic-material baseline.
9. Tune specular, refraction, blur, translucency, and shadow one variable at a time.
10. Disable Effects on opaque or flat layers that should not receive glass.
11. Author Dark with color changes before geometry changes.
12. Author Mono, then inspect Clear and Tinted light/dark over flat and photographic backgrounds.
13. Rotate the lighting angle, toggle the official grid, and inspect several preview sizes.
14. Check iOS/macOS and watchOS layouts separately; record every override.
15. Export a flattened Default image for comparison and marketing if required.
16. Compare the export with the approved concept at 1024 px and 32 px. Return for approval if a protected invariant changed.
17. Save with Icon Composer and retain screenshots of the tested modes.

Do not tune all effects simultaneously. If a result feels wrong, identify whether the failure comes from source geometry, grouping, color, material, or composition and change only that layer of the system.

## Xcode delivery and fallback behavior

Add the `.icon` file to the Xcode target. In the target’s General pane, ensure **App Icons and Launch Screen → App Icon** matches the filename without `.icon`. Multiple Composer files can exist, but only the matching name is selected.

Current Xcode uses the matching Icon Composer file instead of the existing `AppIcon` asset catalog. When the target supports older releases without the same Liquid Glass appearances, Xcode generates fallback icon images from the Composer file at build time.

Consequences:

- preserve the old asset catalog until the Composer build and runtime result are accepted;
- test the oldest supported release when fallback appearance matters;
- keep the asset-catalog route if the exact historical icon must remain unchanged;
- inspect build warnings rather than assuming fallback generation succeeded;
- verify alternate-icon configuration separately.

## Validation matrix

Record direct evidence for every claimed cell:

| Surface | Required observation |
| --- | --- |
| Composer Default | source order, material edges, approved-design fidelity |
| Composer Dark | contrast, color overrides, shadow behavior |
| Composer Mono | luminance hierarchy and identity anchor |
| Clear light/dark | wallpaper transmission and boundary legibility |
| Tinted light/dark | tint resilience and focal hierarchy |
| Lighting angles | moving specular/refraction does not distort identity |
| Small Composer sizes | silhouette and group separation survive |
| watchOS | circular crop and optical position |
| Xcode | selected `.icon`, successful build, no relevant asset warnings |
| Simulator | Home Screen plus requested system surfaces |
| Earlier release | generated fallback, when supported and relevant |
| Physical device | named model and OS; dynamic response where observable |

Composer screenshots validate only the tool preview. Simulator validates only that runtime and context. Neither proves a physical display, App Review, or conversion.

## Failure modes

- Starting layer production before a named whole-icon version is approved
- Generating every layer independently and losing shared geometry or lighting
- Using more than four depth groups
- Confusing imported graphic layers with rendered depth groups
- Applying Individual mode where adjacent pieces must form one silhouette
- Baking mask, bevel, shadow, blur, refraction, or specular into source art
- Making every transparent shape glass
- Using thin, feathered edges that produce weak system highlights
- Treating Default, Dark, Mono, Clear, and Tinted as unrelated identities
- Ignoring the watchOS circular crop
- Editing a `.icon` package by hand and claiming tool validation
- Replacing the asset catalog before testing older-release output
- Calling a static heuristic preview an Icon Composer render
