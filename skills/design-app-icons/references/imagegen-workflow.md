# Imagegen workflow for app-icon concepts

Use the built-in `image_gen` tool by default. Use image generation for new raster concepts and variants; use deliberate vector reconstruction for final scalable source layers.

## Contents

- [Input roles](#input-roles)
- [Concept prompt structure](#concept-prompt-structure)
- [Approval-gated concept loop](#approval-gated-concept-loop)
- [Choose the shortest delivery](#choose-the-shortest-delivery)
- [Layer-first generation](#layer-first-generation)
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

## Approval-gated concept loop

Keep exploration cheap and reversible:

1. Generate flattened whole-icon directions first. Do not generate production layers while the design is unapproved.
2. Save each retained candidate with a stable version such as `concept-a1.png`, `concept-a2.png`, or `concept-b1.png`.
3. Show the selected candidate at 1024 px and 32 px. Ask the user to identify what to preserve and the single most important change.
4. For a revision, prefer built-in Imagegen edit semantics when an existing candidate must remain recognizable. Repeat invariants such as “change only the wave height; preserve silhouette, sun, palette, lighting, and composition.” Generate a new version instead of overwriting the prior candidate.
5. If an edit drifts, return to the last accepted candidate rather than stacking corrections onto the drifted output.
6. Mark every candidate `Exploring — not approved` until the user explicitly names the approved version.

Do not interpret “better,” “almost,” or a lack of criticism as approval. Once the user says a clear equivalent of “approve,” “lock,” “this is the one,” or “proceed with this version,” preserve that version and continue with the shortest requested delivery. For an image-only result, the explicit approval in conversation is enough. Create `assets/design-approval-template.yaml` only for a project-bound editable, Icon Composer, or Xcode handoff.

If the user asks for the entire workflow upfront, complete the concept comparison and pause at the approval gate. After approval, finalize the whole image first. Continue into layers, Composer, or Xcode only when the original request explicitly included that delivery. Ask again when production would visibly change a locked invariant or an external action requires separate authorization.

## Choose the shortest delivery

Use this order after approval:

1. **Finished image — default:** retain the integrated rendering, make only approved cleanup edits, export an opaque 1024 × 1024 PNG, run static QA, and stop.
2. **Flattened platform asset:** preserve the whole image when Xcode integration is requested and exact appearance matters.
3. **Minimal SVG reconstruction:** use for simple geometry, repeatable brand curves, or editable color systems.
4. **Minimal Icon Composer sources:** use only when explicitly requested and the design benefits from independent platform material or depth.

Do not decompose a successful image merely because separate layers sound more professional. A flattened image is often the most faithful production source for integrated 3D lighting, soft bloom, translucent shells, painterly material, fur, glass, or shared reflections.

Before choosing layers, ask one question: `Can these roles be separated and recomposed without changing the approved visual?` If the answer is uncertain, use the finished image. If a proof changes the silhouette, proportions, focal scale, lighting continuity, seam softness, face placement, or palette, reject the decomposition and return to the approved image.

A technically valid alpha set can still be the wrong production route. Reject a separated proof when an integrated glow turns into a detached disk, soft seams harden, proportions drift, or shared lighting breaks.

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

## Layer-first generation

Use this rare route only after explicit approval, only when the user requested independent raster roles, and only when the chosen roles can be separated without losing shared light or material continuity. It is not automatically better than a finished image or vector reconstruction.

### 1. Freeze a composition contract

Before generating layers, copy `assets/layer-composition-template.yaml` and record:

- one square coordinate system, normally 1024 by 1024
- the final bounding box and optical center for each element
- a shared camera, perspective, material vocabulary, palette, and light direction
- back-to-front layer order and which layer must be opaque
- the approved concept path, digest, and locked invariants from `assets/design-approval-template.yaml`

Every generated layer must use that same contract. “Centered” is not precise enough when independently generated objects must align.

### 2. Generate one role per image

Use separate calls for a backdrop, main object, glow or inset, foreground accent, or shadow only when the element needs independent material, appearance, or depth control and the seam is visually independent in the approved image. Do not split every highlight into a layer. Do not isolate a glow that visibly illuminates or passes through another generated material unless a recomposed test already proves that continuity can be retained.

For a foreground element, ask for:

```text
Exact square working canvas using the locked composition contract.
Only <one element>, at final position and scale.
No text, border, tile, presentation scene, or unrelated object.
All other pixels genuinely transparent.
Preserve the shared camera, palette, material, and light direction.
```

### 3. Audit transparency immediately

Do not trust a visible checkerboard. Inspect the actual PNG channel. Image generators may bake a checkerboard into an opaque RGB image or ignore the requested dimensions.

If the file has no alpha:

1. retry the element on a perfectly uniform key color absent from the artwork, such as `#00FF00`;
2. convert that key color to alpha with `scripts/prepare_raster_layer.py` or a reviewed graphics workflow;
3. inspect the edge at 100% for key-color spill and halos;
4. reject the layer if translucent bloom or glass cannot be separated cleanly.

Example:

```bash
python3 scripts/prepare_raster_layer.py raw-shell.png shell.png \
  --key-color 0,255,0 \
  --fit-box 240,64,784,946 \
  --report shell-cleanup.json
```

`--fit-box` deliberately re-establishes the composition contract when generation drifted. This is positioning, not proof that the generated geometry matches the concept.

Treat its output as an **alpha-normalized candidate**, not a clean or approved production layer. Inspect the boundary at 100–400% over black, white, neutral gray, and a saturated color. Reject green/magenta fringe, single-pixel halos, damaged semitransparent edges, and mismatched occlusion seams. Chroma keying is unsuitable when intended glass, bloom, or translucency mixes with the key color; regenerate on another matte, manually author the matte, or reconstruct the element.

### 4. Compose and compare

Composite the alpha-normalized candidates in the intended order before importing them. Compare the result to the approved concept at full size and 32 px. Check silhouettes, seams, occlusion, edge contamination, and whether independent lighting still feels coherent.

Treat small reconstruction corrections as production work, but treat a changed metaphor, silhouette, object relationship, focal scale, palette, or lighting continuity as a new design. Reject the layer route rather than normalizing drift. Return to the approved whole image, or return a deliberately changed concept to the concept loop for re-approval before opening Icon Composer.

Use `scripts/compose_raster_layers.py` for deterministic normal-alpha composition on a shared canvas. It embeds sRGB in the flattened proof. Record each candidate’s original alpha bounds, scale factor, final alpha bounds, center offset, and spill heuristic from `prepare_raster_layer.py`; these metrics help locate drift but do not prove visual alignment.

Raster layers may be imported into Icon Composer when their alpha edges and resolution survive review. Reconstruct as SVG when the identity depends on exact curves, symmetry, repeatable geometry, easy recoloring, or future brand edits. A mixed package is valid: for example, SVG shell plus raster glow.

Classify every effect before handoff:

- **Intrinsic raster texture:** intentional painted grain or material detail that stays in the bitmap.
- **Alpha-edge translucency:** real semitransparent source pixels that must survive edge review on varied backgrounds.
- **Platform material:** refraction, specular response, shadow, and glass depth recreated in Icon Composer rather than baked into the source.

For iOS plus watchOS, do not assume one 1024 px raster is both deliverables. Prefer normalized vector geometry that can be placed in 1024 × 1024 iOS and 1088 × 1088 watchOS layouts within the same groups. For essential raster texture, prepare and audit platform-specific exports or scale once from the larger reviewed source, then apply an explicit circular-crop optical override. Reusing the group does not require reusing identical raster pixels.

### 5. Record failures

Keep the raw outputs only when they teach a reusable limitation. Label opaque checkerboards, alignment drift, or contaminated edges as rejected—not as production layers. Never claim that separate generation alone produced a valid `.icon` document.

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

During the concept phase, after each generation:

1. Inspect at full size.
2. Downsample mentally or with `scripts/icon_qa.py`.
3. Identify one failure: silhouette, scale, palette, depth, or originality.
4. Make one targeted change while repeating invariants.
5. Keep discarded directions only when the user wants a decision trail.
6. Preserve the last accepted candidate and create a new version for every revision.
7. Do not begin layer generation or Composer work until explicit approval is recorded.

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

For the default finished-image or flattened platform deliverable, still remove artifacts, resize with a high-quality filter, verify opacity, embed a supported color profile when needed, and test the actual Xcode result when integration was requested. This is a complete route, not an inferior fallback.

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
