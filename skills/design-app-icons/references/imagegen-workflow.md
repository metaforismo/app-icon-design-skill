# Imagegen workflow for app-icon concepts

Use the built-in `image_gen` tool by default. Use image generation for new raster concepts and variants; use deliberate vector reconstruction for final scalable source layers.

## Contents

- [Input roles](#input-roles)
- [Concept prompt structure](#concept-prompt-structure)
- [Base prompt](#base-prompt)
- [Style recipes](#style-recipes)
- [Iteration](#iteration)
- [Production boundary](#production-boundary)
- [Provenance record](#provenance-record)

## Input roles

Label every supplied image:

- **Edit target:** change the asset while preserving stated invariants.
- **Identity anchor:** preserve the user’s owned mark or character.
- **Style reference:** borrow broad qualities only.
- **Competitive reference:** analyze differentiation; do not feed into generation unless rights and intent are clear.
- **Context screenshot:** understand Home Screen, App Store, Dock, or device scale.

When references contain third-party icons, state: `Use only broad qualities; do not reproduce symbols, composition, colors, characters, or brand identity.`

Do not store or redistribute user-supplied reference images in a public repository without explicit permission.

## Concept prompt structure

Use only lines that improve the result:

```text
Use case: logo-brand
Asset type: original iOS app icon concept for <fictional or user-owned app>
Input images: <index and role>
Product promise: <short phrase>
Primary request: <one metaphor and recognition anchor>
Style/medium: <flat vector-like / tactile 3D / layered glass / mascot>
Composition/framing: exact square artwork, edge-to-edge background, centered focal mark, generous internal margin, readable at 32px
Color palette: <2-4 intentional colors>
Materials/textures: <only if needed>
Constraints: original design; no text by default; no trademarks; no watermark; no device mockup; no surrounding canvas; no baked rounded-square mask; geometry suitable for <=4 depth groups
Avoid: copied reference geometry; tiny detail; stock-logo look; excess glow; illegible reflections
```

The prompt should describe the artwork, not a glossy presentation of an app-icon tile on a desk or wallpaper.

## Base prompt

```text
Use case: logo-brand
Asset type: original iOS app icon concept
Product promise: <promise>
Primary request: Create one memorable symbol based on <metaphor>.
Style/medium: polished vector-like artwork with restrained depth; suitable for deliberate reconstruction as no more than four Icon Composer groups.
Composition/framing: exact square artwork; edge-to-edge background; one centered focal silhouette; generous internal breathing room; recognizable at 32px.
Color palette: <palette>
Constraints: no text, no letters, no trademarks, no watermark, no device mockup, no surrounding presentation canvas, no baked rounded-square mask or outer tile shadow, original design only.
Avoid: micro-details, thin lines, generic stock mark, excessive bloom, copied competitor geometry.
```

## Style recipes

### Tactile object

Describe one reduced object with simplified geometry. Limit seams, labels, controls, and texture. Ask for controlled studio highlights within the object, not a cast shadow around the final icon tile.

### Minimal geometric

Describe a spatial relationship: fold, weave, orbit, stack, reveal, or transform. Use two or three masses and make negative space intentional. Avoid unexplained starbursts and generic infinity loops.

### Expressive mascot

Choose one ownable body silhouette, one facial grammar, and one emotional signal. Use large features and avoid hands, props, or secondary characters unless the product requires them.

### Layered Liquid Glass

Describe source-friendly depth groups and an opaque recognition anchor. Ask for restrained refraction and specular edges. Avoid a composition that is only attractive because of glow.

### Flat brand mark

Use one or two flat colors, no bevel, and no shadows. Ask for vector-friendly geometry. This route is often best for durable recognition and tinted modes.

## Iteration

After each generation:

1. Inspect at full size.
2. Downsample mentally or with `scripts/icon_qa.py`.
3. Identify one failure: silhouette, scale, palette, depth, or originality.
4. Make one targeted change while repeating invariants.
5. Keep discarded directions only when the user wants a decision trail.

Do not solve a weak metaphor with more polish. Return to concept selection.

## Production boundary

An image-generated concept may contain:

- subtle asymmetry
- fake texture or microcopy
- inconsistent perspective
- gradients that cannot be parameterized
- reflections that merge separate layers
- geometry too noisy to export as SVG

Reconstruct the chosen direction. Do not auto-trace and ship without cleanup. The generated bitmap is not proof of Icon Composer compatibility, correct masking, Xcode delivery, or App Store acceptance.

For a pure bitmap/legacy deliverable, still remove artifacts, resize with a high-quality filter, verify opacity, embed a supported color profile when needed, and test the actual Xcode result.

## Provenance record

Save a short record beside each concept:

```yaml
name: <direction>
generated_at: <ISO date>
tool_mode: built-in image_gen
prompt_file: prompt.md
input_roles:
  - style reference supplied by user; not redistributed
rights_note: Original output; third-party references used only for broad visual qualities.
status: concept only; not an Icon Composer file; not device-validated
```

