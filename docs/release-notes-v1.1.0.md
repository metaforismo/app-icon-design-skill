# App Icon Studio Skill 1.1.0

Version 1.1 introduces an approval-gated workflow that avoids premature production work.

## New workflow

1. Generate and compare flattened whole-icon directions.
2. Iterate non-destructively on the selected direction with one targeted change per version.
3. Pause until the user explicitly approves a named concept.
4. Record the approved artifact digest and protected design invariants.
5. Create one production role per SVG or PNG only after approval.
6. Recompose and compare against the approved concept before entering Icon Composer.
7. Return for re-approval if production requires a visible identity change.

The skill continues autonomously through faithful layer creation, Composer, Xcode, Simulator, and requested handoff after approval. It does not request confirmation after every mechanical step.

## Evidence boundary

- **Validated:** approval-gate regression tests; repository and canonical skill validation; existing Quiet Tide Icon Composer/Xcode/Simulator evidence.
- **Prepared:** design-approval record, layer-composition contract, versioned concept loop, and re-approval rules.
- **Not tested:** physical-device rendering, App Review, live App Store experiments, or conversion outcomes.
