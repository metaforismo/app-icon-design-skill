# Delivery and handoff

## Contents

- [Recommended package](#recommended-package)
- [Icon Composer package](#icon-composer-package)
- [Asset-catalog package](#asset-catalog-package)
- [Concept-only package](#concept-only-package)
- [Naming](#naming)
- [Handoff checklist](#handoff-checklist)

## Recommended package

```text
app-icon/
├── brief.md
├── provenance.yaml
├── concepts/
│   ├── direction-a.png
│   └── direction-b.png
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
│   └── appearance-matrix/
└── qa/
    ├── audit.json
    ├── build.txt
    └── status.md
```

Use only applicable files. Do not fabricate a `.icon` file when Icon Composer was not used.

## Icon Composer package

Deliver:

- editable vector source
- exported SVG/PNG layers
- `.icon` file from Icon Composer
- flattened marketing export
- screenshots of platform and appearance previews
- Xcode target association
- build/runtime evidence

Document group order and any per-platform overrides. Keep source art separate from the `.icon` file.

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
- Keep platform/appearance in variant filenames, for example `app-icon-ios-dark.png`.
- Keep generated raw output separate from cleaned production art.

## Handoff checklist

- [ ] Product promise and target platforms recorded
- [ ] Rights and source roles recorded
- [ ] Selected direction and rejected risks explained
- [ ] Final prompt and generation mode recorded
- [ ] Editable production source present
- [ ] Unmasked layers exported
- [ ] Platform sizes verified
- [ ] Small-size previews present
- [ ] Appearance/mask matrix reviewed
- [ ] Xcode source selected
- [ ] Build succeeds
- [ ] Simulator/device status explicit
- [ ] Store status explicit
- [ ] Unverified claims labeled

