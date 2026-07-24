---
name: design-app-icons
description: Design, redesign, critique, generate, reconstruct, validate, and deliver distinctive app icons, with deep support for iOS, iPadOS, macOS, watchOS, Apple Icon Composer, Liquid Glass, Xcode asset catalogs, alternate icons, and App Store icon experiments. Use when Codex needs to turn a product brief or visual references into original icon directions; use imagegen for bitmap concept exploration or variants; plan production-ready SVG/PNG layers; audit an existing icon at small sizes and across masks or appearances; prepare an Icon Composer or legacy asset-catalog handoff; or document evidence for App Store delivery.
---

# Design App Icons

Create an icon as a product identity system, not a decorated square. Move from a clear product metaphor through original concepts, production layers, platform previews, and an evidence-backed handoff.

## Start with the correct route

Choose one route before creating files:

1. **New icon:** define the app promise, generate distinct metaphors, select one silhouette, then produce and validate.
2. **Redesign:** preserve the recognition anchors that still serve the brand; change only the weaknesses the audit proves.
3. **Critique:** inspect the supplied asset and contexts; return prioritized findings and experiments without changing files unless asked.
4. **Liquid Glass migration:** separate source artwork into layers, remove baked effects, assemble in Icon Composer, and test current appearances.
5. **Delivery or repair:** inspect the Xcode project, existing `.icon` file or asset catalog, platform targets, and build settings before editing.
6. **Experiment design:** create meaningfully different hypotheses and prepare alternate icons for Product Page Optimization without promising lift.

Read the matching reference before acting:

- Platform facts and sizes: [platform-specifications.md](references/platform-specifications.md)
- Liquid Glass and Icon Composer: [liquid-glass-icon-composer.md](references/liquid-glass-icon-composer.md)
- Image generation workflow and prompt recipes: [imagegen-workflow.md](references/imagegen-workflow.md)
- Visual directions and originality: [visual-language.md](references/visual-language.md)
- QA, previews, and evidence: [qa-and-evidence.md](references/qa-and-evidence.md)
- App Store testing: [app-store-experimentation.md](references/app-store-experimentation.md)
- Handoff structure: [delivery-and-handoff.md](references/delivery-and-handoff.md)
- Current sources and claim boundaries: [sources.md](references/sources.md)

## Establish the brief

Collect only information that changes the design:

- app name, category, and the core promise in one short phrase
- target platforms and minimum OS releases
- primary audience and desired emotional signal
- existing brand assets, recognition anchors, and prohibited changes
- required styles or references and the role of each reference
- whether the result is exploration, a flattened bitmap, layer sources, an Icon Composer handoff, or an Xcode change
- legal or policy constraints, including third-party brands, hardware, characters, and licensed art

If the user supplies many references, group them by broad traits instead of imitating individual icons. Label each input as an edit target, identity anchor, style reference, competitive reference, or context screenshot. Never assume a source URL or screenshot grants reuse rights.

When the brief is incomplete but safe to infer, state the assumptions and continue. Ask only when a missing choice would materially change brand identity, platform delivery, or external publication.

## Define the concept before styling it

Write a one-line concept equation:

`product promise + distinctive metaphor + emotional signal`

Then create three genuinely different directions. Vary the metaphor or silhouette, not merely the color:

- **Literal object:** a reduced physical metaphor for a concrete utility
- **Abstract system:** a geometric relationship that expresses motion, connection, focus, or transformation
- **Character or emblem:** an ownable personality or symbolic mark

For each direction, record:

- the idea in seven words or fewer
- the recognition anchor
- why it fits the product
- the main collision risk with competitors or platform icons
- how it survives at small size
- a plausible layer plan of no more than four Icon Composer groups

Reject a direction when its value depends on tiny detail, text, a screenshot, a copied logo, an Apple hardware replica, or effects that disappear when flattened.

## Use imagegen for original concept exploration

Use the built-in `image_gen` tool by default. Read [imagegen-workflow.md](references/imagegen-workflow.md) before generating.

Treat user-supplied icons as references unless the user explicitly asks to edit one. In the prompt, name the broad qualities to borrow and explicitly prohibit reproducing the reference symbol, composition, palette, or brand identity.

Generate one asset per call. For each direction:

1. Write a structured prompt with use case, asset type, product promise, metaphor, style, composition, palette, material, constraints, and avoid list.
2. Require an exact square, edge-to-edge artwork composition with no surrounding presentation canvas.
3. Require one bold focal silhouette, generous internal breathing room, no text by default, no watermark, no trademarks, and no device mockup.
4. Ask for no baked outer rounded-square mask. The platform applies the final mask.
5. If the concept targets Icon Composer, request geometry that can be reconstructed into at most four depth groups.
6. Inspect the result at full size and as a small thumbnail. Iterate with one targeted change.
7. Save project-bound outputs inside the project. Record the final prompt, tool mode, date, input roles, and known limitations.

Do not present an image-generated bitmap as editable vector geometry or as a valid `.icon` file. Use it as a concept master, then reconstruct intentional paths and layers in a vector tool when the delivery requires scalable, brand-controlled artwork.

## Reconstruct production artwork

Use the selected concept as guidance, not as an object to auto-trace blindly.

1. Redraw the defining silhouette with deliberate curves, optical centering, and stable negative space.
2. Remove generation artifacts, accidental asymmetry, noisy texture, fake microcopy, and unrepeatable reflections.
3. Separate only the elements that need independent color, material, platform, appearance, or z-depth control.
4. Convert essential text to outlines, but prefer removing text unless it is a true brand mnemonic.
5. Export unmasked full-canvas SVG layers when supported; use PNG only for artwork that relies on unsupported SVG features.
6. Name source layers back-to-front with numeric prefixes.
7. Keep a flattened concept preview separate from production layer sources.

For current iOS, iPadOS, macOS, and watchOS Liquid Glass work, continue with [liquid-glass-icon-composer.md](references/liquid-glass-icon-composer.md). For tvOS, visionOS, or deliberate legacy delivery, use [platform-specifications.md](references/platform-specifications.md) and [delivery-and-handoff.md](references/delivery-and-handoff.md).

## Validate before calling the icon complete

Run deterministic inspection when Pillow is available:

```bash
python scripts/icon_qa.py path/to/icon.png \
  --platform ios \
  --role flattened \
  --preview-dir work/icon-previews \
  --report work/icon-audit.json
```

Use `--role layer` for transparent source layers. Treat the script as a preflight aid, not a replacement for Icon Composer, Xcode, Simulator, a real device, or visual judgment.

Perform all applicable checks:

- concept still reads at 16, 20, 29, 40, 60, 76, 83, 128, and 256 pixels
- essential content remains legible under the platform mask and official grid
- no accidental pre-masking, clipped content, transparent corners in a flattened iOS master, or edge halo
- Default, Dark, Mono, Clear light/dark, and Tinted light/dark previews retain the recognition anchor where supported
- glass, specular, refraction, shadows, and translucency remain restrained and intentional
- round watchOS and visionOS crops preserve optical centering
- icon is distinguishable from adjacent category competitors without borrowing their marks
- Xcode target settings point to the intended icon source
- Simulator and real-device results are documented separately from static previews

If a context was not tested, say `not tested`; do not convert a design assumption into evidence.

## Handle platform files safely

Before modifying an app:

1. Inspect the project, targets, current `AppIcon` asset catalog, `.icon` files, build settings, alternate icon configuration, and minimum deployments.
2. Preserve existing sources until the new path builds and displays correctly.
3. Remember that adding an Icon Composer file can replace the existing app icon asset catalog for the target.
4. Use the current Xcode-generated result for older releases only if the user accepts that rendering. Keep asset catalogs when the exact historical artwork must remain.
5. Do not hand-author an undocumented `.icon` package or claim that a renamed directory is an Icon Composer file.
6. Keep tvOS and visionOS asset-catalog workflows separate from Icon Composer delivery.

Use Xcode-native build and simulator tools when available. Verify active project, scheme, and simulator defaults before the first build or run.

## Prepare experiments honestly

For Product Page Optimization, vary one meaningful hypothesis at a time. Examples:

- literal utility versus abstract brand signal
- calm low-contrast palette versus high-salience palette
- character warmth versus geometric precision

Keep the product promise and visual quality comparable. Ensure alternate icons are included in the submitted binary when required. Report impressions, conversion outcomes, uncertainty, and the test window; do not claim rankings or conversion lift from aesthetic preference alone. Read [app-store-experimentation.md](references/app-store-experimentation.md).

## Deliver a reproducible handoff

Use the templates in `assets/` and include:

- approved brief and assumptions
- concept directions and selection rationale
- final prompt history and image-generation provenance
- concept master and separated production sources
- layer order and intended Icon Composer settings
- platform and appearance matrix
- deterministic audit report and small-size previews
- Xcode/Simulator/device evidence
- known limitations and untested states
- source links with access date

End with a concise status split:

- **Validated:** directly observed or tool-verified
- **Prepared:** files exist but need platform import or build
- **Not tested:** external, device, App Store, or conversion claims not verified

