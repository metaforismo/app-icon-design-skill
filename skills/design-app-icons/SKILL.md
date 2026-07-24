---
name: design-app-icons
description: Design, redesign, critique, generate, validate, and optionally productionize distinctive app icons, with deep support for iOS, iPadOS, macOS, watchOS, Apple Icon Composer, Liquid Glass, Xcode asset catalogs, alternate icons, and App Store icon experiments. Use when Codex needs to turn a product brief or visual references into original whole-icon Imagegen directions; iterate until the user explicitly approves one; finish a high-fidelity 1024 px image by default; choose flattened asset delivery, minimal editable reconstruction, or Icon Composer only when the user requests it and the route can preserve the approved design; audit an icon at small sizes and across masks or appearances; or document App Store delivery and experimentation.
---

# Design App Icons

Create an icon as a product identity system, not a decorated square. Use the shortest route that preserves the approved artwork. Iterate on one finished whole-icon image first. By default, deliver that image after approval and static QA. Create editable layers, enter Icon Composer, or modify Xcode only when the user explicitly requests that additional delivery and the route will not degrade the design.

## Start with the correct route

Choose one route before creating files:

1. **New icon:** define the app promise, generate distinct metaphors, iterate on one silhouette, obtain explicit approval, then finalize the whole image. Stop there unless the user requests platform production.
2. **Redesign:** preserve the recognition anchors that still serve the brand; iterate on the weaknesses the audit proves, obtain explicit approval, then finalize the approved image.
3. **Critique:** inspect the supplied asset and contexts; return prioritized findings and experiments without changing files unless asked.
4. **Liquid Glass migration:** use only for explicitly requested, already-approved platform production. Separate the minimum viable source roles, assemble in Icon Composer, and test current appearances.
5. **Delivery or repair:** inspect the Xcode project, existing `.icon` file or asset catalog, platform targets, and build settings before editing.
6. **Experiment design:** create meaningfully different hypotheses and prepare alternate icons for Product Page Optimization without promising lift.
7. **Plan only:** specify directions, prompts, gates, file structure, and evidence boundaries without invoking Imagegen or claiming files exist.

Read the matching reference before acting:

- Platform facts and sizes: [platform-specifications.md](references/platform-specifications.md)
- Liquid Glass and Icon Composer: [liquid-glass-icon-composer.md](references/liquid-glass-icon-composer.md)
- Image generation workflow and prompt recipes: [imagegen-workflow.md](references/imagegen-workflow.md)
- Visual directions and originality: [visual-language.md](references/visual-language.md)
- QA, previews, and evidence: [qa-and-evidence.md](references/qa-and-evidence.md)
- App Store testing: [app-store-experimentation.md](references/app-store-experimentation.md)
- Handoff structure: [delivery-and-handoff.md](references/delivery-and-handoff.md)
- Current sources and claim boundaries: [sources.md](references/sources.md)

## Use the shortest fidelity-first flow

Use this sequence by default for new icons and redesigns:

`Brief → whole-icon concepts → targeted revisions → explicit approval → final whole image → static QA → stop`

This is the complete default workflow. Do not treat layers or Icon Composer as a mandatory definition of “finished.”

### Phase 1 — Explore and iterate

1. Generate whole-icon concept masters, not production layers.
2. Present clearly named directions or versions at full size and small-icon scale.
3. Ask what to keep and what to change. On each revision, edit the selected concept or generate a targeted successor while repeating its locked invariants.
4. Change one design dimension at a time when practical: metaphor, silhouette, composition, palette, depth, or material.
5. Keep the phase status `Exploring — not approved`; do not create SVG production geometry, transparent layer sets, `.icon` files, Xcode changes, or Composer evidence yet.
6. Continue until the user explicitly approves a specific version.

End each concept turn with the version IDs shown, a one-line description of what changed, and a direct choice: request another targeted revision or explicitly approve one named version. Do not make the user restate the whole brief.

Do not infer approval from silence, “better,” “interesting,” or a request for another variation. Accept clear equivalents such as “I approve this,” “this is the one,” “lock this design,” or “proceed to production with version B3.” If the user supplies an already-approved design and asks to finish or integrate it, record that as the approval and choose the applicable Phase 2 route.

### Gate 1 — Lock the approved image

Record the user’s explicit approval in the conversation and preserve the named image version. For the default image-only route, this is sufficient: finalize that image, audit it, and stop.

Create `assets/design-approval-template.yaml` only for a project-bound production handoff that will create editable geometry, layers, Icon Composer, or Xcode changes. Record:

- the approved concept path or supplied source and its SHA-256 digest when a local file exists
- the exact approved version and approval date
- recognition anchor, silhouette, composition, palette, and protected invariants
- permitted production translations, such as replacing baked glass with Composer material
- the selected delivery route and, only when applicable, the minimal back-to-front layer plan

Set `status: approved-production-authorized`, `approval.explicitly_approved: true`, and `production_plan.authorized: true` only when the user authorized project-bound production. When the approved source is not a local file, keep `concept.sha256: null` and describe the supplied source precisely in the evidence note; never invent a digest.

For image-only finalization, change nothing unless the user requested cleanup. For optional production routes, the approval locks the design intent, not incidental generation artifacts: repair only what the delivery requires, and never silently change the approved identity.

### Phase 2 — Choose one post-approval delivery route

Choose the least complex route that satisfies the request:

1. **Image-only — default.** Preserve the approved whole image. Make only requested cleanup edits, export an opaque unmasked 1024 × 1024 PNG, run static QA, create small-size previews, and stop. Do not create layers or open Icon Composer.
2. **Flattened platform delivery.** Use when the user requests app integration and exact pixel fidelity matters more than dynamic materials. Preserve the whole approved image and integrate it through the applicable supported asset-catalog or Xcode workflow. Do not decompose it merely to claim editability.
3. **Minimal editable reconstruction.** Use when the design is simple geometric artwork or the user needs durable brand-controlled sources. Reconstruct deliberate SVG geometry with the fewest independent roles that preserve the design.
4. **Minimal Icon Composer delivery.** Use only when the user explicitly requests Liquid Glass or a current multilayer Apple handoff and the approved artwork can survive separation. Prefer one to three logical roles; never split every visible highlight, seam, or glow.

For routes 3 and 4, freeze the coordinate, lighting, palette, and optical-alignment contract; recompose the sources; and compare the proof with the approved image at full size and 32 px. If fidelity is worse, stop and use route 1 or 2 unless the user explicitly approves a changed concept. Do not keep repairing a degraded decomposition.

Treat integrated soft lighting, shared reflections, translucent glow bleeding through a shell, painterly shading, fur, glass, and organic material continuity as strong signals for a flattened image. A generated image may be a successful final visual even when it is a poor layer source.

The Mood Lantern example is the canonical negative case: its approved concept has continuous shell shading and an integrated amber glow. Separating the shell and glow produced harder rings, a detached luminous disk, altered proportions, changed face placement, and less coherent lighting. The correct fidelity-first route is the approved whole image, not the assembled proof.

Keep intermediate status explicit:

- `Exploring — not approved`: concept iterations only
- `Approved — image finalization authorized`: the selected whole image may be finalized and audited
- `Approved — production authorized`: a recorded project-bound handoff may proceed through the specifically requested route
- `Production blocked — re-approval required`: faithful reconstruction is not possible without a visible design change

## Establish the brief

Collect only information that changes the design:

- app name, category, and the core promise in one short phrase
- target platforms and minimum OS releases
- primary audience and desired emotional signal
- existing brand assets, recognition anchors, and prohibited changes
- required styles or references and the role of each reference
- whether the result is exploration or the default finished image; ask about layers, Icon Composer, or Xcode only when the user requested production delivery
- whether a specific concept is already explicitly approved for production; assume `no` when unclear
- legal or policy constraints, including third-party brands, hardware, characters, and licensed art

If the user supplies many references, group them by broad traits instead of imitating individual icons. Label each input as an edit target, identity anchor, style reference, competitive reference, or context screenshot. Never assume a source URL or screenshot grants reuse rights.

When the brief is incomplete but safe to infer, state the assumptions and continue. Ask only when a missing choice would materially change brand identity, platform delivery, or external publication.

For plan-only requests, do not generate or write assets. Use `Prepared (specification only)` for a reproducible plan and state plainly that no files exist.

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
- a plausible delivery route: whole image, flattened platform asset, minimal SVG, or minimal Icon Composer

Reject a direction when its value depends on tiny detail, text, a screenshot, a copied logo, an Apple hardware replica, or effects that disappear when flattened.

## Use imagegen for original concept exploration

Use the built-in `image_gen` tool by default. Read [imagegen-workflow.md](references/imagegen-workflow.md) before generating.

Treat user-supplied icons as references unless the user explicitly asks to edit one. In the prompt, name the broad qualities to borrow and explicitly prohibit reproducing the reference symbol, composition, palette, or brand identity.

During Phase 1, optimize for decision speed. Generate or edit a single flattened whole-icon candidate per call. Do not spend calls generating separate background, symbol, glow, shadow, or texture layers before approval. Preserve each selected candidate as a versioned concept master so the user can compare and revise it non-destructively.

Generate one asset per call. For each direction:

1. Write a structured prompt with use case, asset type, product promise, metaphor, style, composition, palette, material, constraints, and avoid list.
2. Require an exact square, edge-to-edge artwork composition with no surrounding presentation canvas.
3. Require one bold focal silhouette, generous internal breathing room, no text by default, no watermark, no trademarks, and no device mockup.
4. Ask for no baked outer rounded-square mask. The platform applies the final mask.
5. Only if the user explicitly requests Icon Composer, favor geometry that can be reconstructed into at most four depth groups without losing its character.
6. Inspect the result at full size and as a small thumbnail. Iterate with one targeted change while preserving all stated invariants.
7. Save project-bound outputs inside the project. Record the final prompt, tool mode, date, input roles, and known limitations.

Do not present an image-generated bitmap as editable vector geometry or as a valid `.icon` file. It can still be the approved final image. Reconstruct intentional paths and layers only when the requested delivery requires scalable, brand-controlled artwork and reconstruction preserves fidelity.

Only after Gate 1, and only when the user explicitly requests separate raster roles, use the rare layer-first route in [imagegen-workflow.md](references/imagegen-workflow.md). Start from `assets/layer-composition-template.yaml`, verify actual alpha, and composite a proof before import. Abandon this route when shared lighting, bloom, reflections, or soft seams no longer match the approved image. If Imagegen returns a baked checkerboard or drifts in placement, retry against a flat key color or reconstruct; never call the raw result transparent or aligned without checking it.

## Reconstruct production artwork only when selected

Begin only after Gate 1 and only for delivery route 3 or 4. Use the approved concept and approval record as the visual contract, not as an object to auto-trace blindly.

1. Redraw the defining silhouette with deliberate curves, optical centering, and stable negative space.
2. Remove generation artifacts, accidental asymmetry, noisy texture, fake microcopy, and unrepeatable reflections.
3. Separate only the elements that need independent color, material, platform, appearance, or z-depth control. Keep integrated glow and lighting with the artwork that creates them.
4. Convert essential text to outlines, but prefer removing text unless it is a true brand mnemonic.
5. Export unmasked full-canvas SVG layers when supported; use PNG only for artwork that relies on unsupported SVG features.
6. Name source layers back-to-front with numeric prefixes.
7. Keep a flattened concept preview separate from production layer sources.
8. Recompose the sources after every material layer change and compare them against the approved concept before continuing. Revert to a flattened route when the proof is visibly worse.

For explicitly requested current iOS, iPadOS, macOS, and watchOS Liquid Glass work, continue with [liquid-glass-icon-composer.md](references/liquid-glass-icon-composer.md). For tvOS, visionOS, flattened artwork, or deliberate legacy delivery, use [platform-specifications.md](references/platform-specifications.md) and [delivery-and-handoff.md](references/delivery-and-handoff.md).

## Validate before calling the icon complete

Run deterministic inspection when Pillow is available:

```bash
python3 scripts/icon_qa.py path/to/icon.png \
  --platform ios \
  --role flattened \
  --preview-dir work/icon-previews \
  --report work/icon-audit.json
```

Use `--role layer` for transparent source layers. Treat the script as a preflight aid, not a replacement for Icon Composer, Xcode, Simulator, a real device, or visual judgment.

The preview sheet preserves tvOS aspect ratio, applies an approximate platform mask, and includes light, dark, mono, and tinted stress-test columns. Never label those simulations as Apple-rendered appearances.

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

Do not begin Icon Composer or Xcode integration for an unapproved concept or an image-only request. After explicit approval and a request for platform integration, inspect the target before modifying an app:

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

For the default image-only handoff, include only the approved 1024 px image, prompt/provenance, static audit, small-size previews, and explicit status. Use the additional templates in `assets/` only for a requested project-bound production handoff, then include:

- approved brief and assumptions
- approval record, approved concept digest, and locked invariants
- concept directions and selection rationale
- final prompt history and image-generation provenance
- concept master and separated production sources only when the selected route requires them
- layer order and intended Icon Composer settings
- platform and appearance matrix
- deterministic audit report and small-size previews
- Xcode/Simulator/device evidence
- known limitations and untested states
- source links with access date

End with a concise status split. `Prepared` may describe either existing artifacts or a reproducible specification; qualify the latter as `Prepared (specification only)` so the user never infers files exist:

- **Validated:** directly observed or tool-verified
- **Prepared:** files exist but need platform import or build
- **Not tested:** external, device, App Store, or conversion claims not verified
