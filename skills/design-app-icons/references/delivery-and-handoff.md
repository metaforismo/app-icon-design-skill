# Delivery and handoff

## Contents

- [Recommended package](#recommended-package)
- [Finished-image package](#finished-image-package)
- [Icon Composer package](#icon-composer-package)
- [Asset-catalog package](#asset-catalog-package)
- [Concept-only package](#concept-only-package)
- [Naming](#naming)
- [Handoff checklist](#handoff-checklist)

## Recommended package

Use the smallest package that matches the request. The full tree below is the default for a shipping iOS, iPadOS, macOS, or watchOS icon; concept-only requests stop before production.

```text
app-icon/
├── brief.md
├── provenance.yaml
├── design-approval.yaml
├── concepts/
│   ├── direction-a1.png
│   ├── direction-a2.png
│   └── direction-b1.png
├── production/
│   ├── source.fig-or-ai-or-sketch
│   ├── layers/
│   │   ├── 01-background.svg
│   │   ├── 02-symbol.svg
│   │   └── 03-accent.svg
│   ├── AppIcon.icon
│   └── flattened/
│       └── app-icon-1024.png
├── previews/
│   ├── small-sizes/
│   ├── appearance-matrix/
│   └── context-board/
└── qa/
    ├── audit.json
    ├── build.txt
    └── status.md
```

Use only applicable files. Keep `design-approval.yaml` in `exploring-not-approved` state for a concept-only handoff. Do not create production sources or fabricate a `.icon` file when explicit approval and Icon Composer use have not occurred.

## Finished-image package

Use this only when the request explicitly ends at an approved image or when the user selects the flattened fallback:

```text
app-icon/
├── app-icon-1024.png
├── prompt.md
├── provenance.yaml
├── previews/
│   └── small-sizes/
└── qa/
    ├── audit.json
    └── status.md
```

Preserve the approved integrated rendering. State `Composer not used` and why. Do not add an editable source, `.icon` document, build log, or device claim that was not validated.

## Icon Composer package

Deliver:

- approved concept and completed `design-approval.yaml`
- editable vector source
- exported SVG/PNG layers
- `.icon` file from Icon Composer
- flattened marketing export
- screenshots of platform and appearance previews
- screenshots over multiple backgrounds, lighting angles, and small Composer sizes
- Xcode target association
- build/runtime evidence

Document the maximum-four-group structure, group mode (Individual or Combined), material decisions, appearance overrides, and platform overrides. Keep source art separate from the `.icon` file.

## Asset-catalog package

Prefer letting Xcode create the icon set. Deliver:

- required source images
- existing Xcode-generated `AppIcon.appiconset` or platform image stack
- `Contents.json` generated or updated through the supported Xcode structure
- Any/Dark/Tinted variants where applicable
- alternate icon source names and configuration
- build evidence

Do not overwrite an existing catalog before preserving it. Do not assume a generic `Contents.json` fits every target.

## Concept-only package

Deliver:

- final prompt
- generated bitmap
- a design critique
- recommended vector layer plan
- explicit status: `concept only; not Icon Composer or device validated`

This is a valid handoff when the user requested ideation rather than platform integration.

## Naming

- Use lowercase hyphenated filenames for exports.
- Use numeric prefixes for layer z-order.
- Use stable direction names instead of `final-final-2`.
- Version concept iterations before approval, for example `direction-a1.png`, `direction-a2.png`, and `direction-b1.png`.
- Keep platform/appearance in variant filenames, for example `app-icon-ios-dark.png`.
- Keep generated raw output separate from alpha-normalized candidates and approved production art.

## Handoff checklist

- [ ] Product promise and target platforms recorded
- [ ] Rights and source roles recorded
- [ ] Selected direction and rejected risks explained
- [ ] Explicit approval, approved version, artifact digest, and protected invariants recorded
- [ ] Composer-feasibility result recorded: faithful, adapted concept re-approved, or flattened fallback selected
- [ ] Production composite compared with the approved concept at full size and 32 px when layers exist
- [ ] Final prompt and generation mode recorded
- [ ] Editable production source present when requested
- [ ] Unmasked layers exported when requested
- [ ] Platform sizes verified
- [ ] Small-size previews present
- [ ] Synthetic context board reviewed
- [ ] Appearance/mask matrix reviewed
- [ ] Composer backgrounds, lighting angles, and preview sizes reviewed
- [ ] Xcode source selected when integration was requested
- [ ] Build succeeds when integration was requested
- [ ] Simulator/device status explicit
- [ ] Store status explicit
- [ ] Unverified claims labeled
