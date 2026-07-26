# App Icon Studio 2.0.0

Version 2 turns the repository from an image-first library with optional production into an approval-gated design-to-Icon-Composer workflow.

## Creative loop

1. Establish a short brief and inspect current category collisions.
2. Generate one complete direction for a precise brief or at most two when the identity is unresolved.
3. Review stable versions at full size and 32 px.
4. Change one requested variable while preserving named invariants.
5. Pause until the user explicitly approves a named version.

The same gate now applies to App Icon Studio’s own generated branding. This release preserves the existing identity; it does not silently replace it.

## Production loop

For compatible shipping iOS, iPadOS, macOS, and watchOS icons, the workflow now continues through:

1. Composer-feasibility assessment.
2. Deliberate SVG/PNG reconstruction.
3. Full-size and 32 px fidelity comparison.
4. Real Apple Icon Composer authoring with no more than four semantic depth groups.
5. Default, Dark, Mono, Clear, and Tinted review across backgrounds, lighting angles, and sizes.
6. Xcode target association, build, and requested runtime contexts.

If a protected visual invariant must change, the skill returns a named Composer-adapted concept for approval. If the user prioritizes exact complex illustration, the flattened fallback remains available and is labeled `Composer not used`.

## Tooling

`icon_qa.py` now adds a deterministic 1200 × 760 synthetic context board beside its size and appearance outputs. It uses generic neighboring tiles to test salience in light/dark grids, search/Settings-style rows, and notification-badge occlusion without redistributing third-party icons.

## Evidence

- **Validated in this release:** repository validator, unit tests, canonical skill validation, deterministic packaging, four static example audits, QA context-board generation, and a successful Xcode 26.6 rebuild of the existing Quiet Tide `.icon` fixture.
- **Previously validated fixture evidence retained:** Icon Composer 1.6 appearance captures and the iOS 26.5 Simulator Home Screen observation named in the Quiet Tide ledger.
- **Prepared:** the revised workflow, templates, Composer guidance, and installable v2 skill.
- **Not tested for new artwork:** a new Composer document, new Xcode integration, physical device, App Store submission/review, or conversion outcome.
