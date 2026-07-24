# Changelog

## 1.2.0 — 2026-07-24

- Made the approved finished image plus static QA the complete default deliverable.
- Replaced mandatory post-approval layer production with four explicit routes: image-only, flattened platform delivery, minimal SVG, and minimal Icon Composer.
- Added a fidelity gate that rejects decomposition when proportions, seams, glow, lighting continuity, or recognition anchors drift.
- Reclassified Mood Lantern’s layer-first assembly as a negative example and documented why integrated rendering should remain flattened.
- Replaced the exploded technical social preview with a single finished-icon presentation.
- Updated routing tests, repository validation, handoff guidance, and skill metadata for the shorter workflow.

## 1.1.0 — 2026-07-24

- Added an explicit two-phase workflow: inexpensive whole-icon iteration first, production only after user approval.
- Added stable concept versioning, edit invariants, approval language, and a rule against inferring approval from vague positive feedback.
- Added a machine-readable design-approval template with artifact digest, design lock, permitted translations, layer decisions, and re-approval triggers.
- Required approved-concept comparison before Icon Composer and a return to concept approval whenever reconstruction materially changes the identity.
- Added regression tests and repository validation for the approval gate.

## 1.0.0 — 2026-07-24

- Added the production-oriented `$design-app-icons` Codex skill.
- Added current Apple-platform, Icon Composer, Liquid Glass, delivery, QA, originality, and Product Page Optimization references.
- Added four original Imagegen case studies and a documented rejected direction.
- Added a real Quiet Tide Icon Composer document, SVG sources, XcodeGen fixture, build evidence, Simulator evidence, and clean Composer export.
- Added the Mood Lantern layer-first Imagegen workflow with honest alpha-failure evidence, chroma cleanup, and compositing tools.
- Added static icon QA, appearance/mask previews, repository validation, tests, CI, and scheduled official-source checks.
- Added deterministic release packaging and an original repository social preview.
