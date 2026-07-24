# App Icon Studio

Design distinctive app icons, explore original directions with image generation, reconstruct clean production layers, and validate the result across Apple platforms.

This repository contains the installable [`design-app-icons`](skills/design-app-icons/SKILL.md) Codex skill, current Apple platform guidance, a deterministic bitmap preflight tool, and four original image-generated case studies.

> Current-source snapshot: **23 July 2026**. Apple’s icon tooling is active and versioned; the skill tells agents to re-check official documentation before release work.

## What makes this different

- **Concept before surface:** start from the app promise and one ownable silhouette.
- **Imagegen with boundaries:** use generated bitmaps for fast, original concept exploration—not as fake vector or `.icon` files.
- **Current Liquid Glass workflow:** prepare SVG/PNG layers, use at most four Icon Composer groups, and validate current refraction/specular behavior.
- **Platform-aware delivery:** distinguish Icon Composer from tvOS/visionOS asset catalogs and exact legacy-art requirements.
- **Evidence, not vibes:** separate static preflight, Icon Composer, Xcode build, Simulator, device, store, and experiment evidence.
- **Honest ASO testing:** design meaningful Product Page Optimization hypotheses without promising ranking or conversion lift.

## Original example directions

The examples were generated with the built-in image-generation tool from original fictional briefs. User-supplied icons informed only broad visual families and are not redistributed.

| Quiet Tide | Parcel Pulse |
| --- | --- |
| [![Quiet Tide concept](examples/quiet-tide/concept-master.png)](examples/quiet-tide/case-study.md) | [![Parcel Pulse concept](examples/parcel-pulse/concept-master.png)](examples/parcel-pulse/case-study.md) |
| Layered abstract identity: one wave, one sun, one silhouette. | Tactile utility metaphor: one parcel, one scan action. |

| Mood Lantern | Orbit Stack |
| --- | --- |
| [![Mood Lantern concept](examples/mood-lantern/concept-master.png)](examples/mood-lantern/case-study.md) | [![Orbit Stack concept](examples/orbit-stack/concept-master.png)](examples/orbit-stack/case-study.md) |
| Expressive mascot: calm emotion and one luminous core. | Liquid Glass system: three layers and one bright anchor. |

Each case study includes the full prompt, rationale, reconstruction plan, limitations, and provenance. These are **concept masters**, not Icon Composer files and not device-validated shipping icons.

Quiet Tide also includes a small [teaching SVG layer pack](examples/quiet-tide/layer-plan.md) that removes baked generative effects and demonstrates unmasked source geometry. It is deliberately not a fabricated `.icon` document.

## Install

Copy the installable skill folder into Codex’s skill directory:

```bash
cp -R skills/design-app-icons "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then invoke it explicitly:

```text
Use $design-app-icons to create three original icon directions for a private journaling app.
```

Example requests:

- “Audit this existing iOS icon at small sizes and explain what actually needs redesign.”
- “Use these screenshots only as style references and generate an original icon.”
- “Plan SVG layers for Icon Composer and test Default, Dark, Clear, and Tinted appearances.”
- “Migrate this Xcode project from `AppIcon.appiconset` to an `.icon` file without losing the old artwork.”
- “Create three Product Page Optimization icon hypotheses and define what evidence would select a winner.”

## Repository map

```text
.
├── skills/design-app-icons/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   ├── references/
│   └── scripts/icon_qa.py
├── examples/
├── docs/
├── scripts/validate_repo.py
└── tests/
```

The skill itself stays progressively disclosed: the core workflow is in `SKILL.md`; detailed Apple specifications, Liquid Glass behavior, prompt recipes, visual taxonomy, QA, App Store experiments, delivery, and source boundaries live in focused references.

## Static preflight

Install the development dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Audit an opaque iOS concept and create small-size previews:

```bash
python skills/design-app-icons/scripts/icon_qa.py \
  examples/quiet-tide/concept-master.png \
  --platform ios \
  --role concept \
  --preview-dir work/quiet-tide-previews \
  --report work/quiet-tide-audit.json
```

The script checks static dimensions and alpha, flags suspicious edge complexity, and generates previews. It cannot validate Icon Composer material, the `.icon` document, Xcode target selection, Simulator, hardware, App Store review, or conversion.

## Validate the repository

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python /path/to/skill-creator/scripts/quick_validate.py skills/design-app-icons
```

CI runs the repository validator and tests. The last command is the canonical Codex skill validator and requires a local Codex installation.

## Source and legal boundaries

- Apple’s HIG, developer documentation, videos, and App Store Connect Help are the authority for current platform claims.
- Secondary articles are inspiration and hypotheses, not authoritative Xcode specifications.
- Apple Design Resources are linked rather than bundled.
- The 61 user-supplied icon references are not committed.
- Do not reproduce another developer’s icon, name, character, product, or Apple hardware.
- Following the workflow does not guarantee App Review approval or conversion improvement.

See [Research notes](docs/research-notes.md), [Example methodology](examples/README.md), and the skill’s [source ledger](skills/design-app-icons/references/sources.md).

## License

Code, documentation, and original example assets are available under the [MIT License](LICENSE), to the extent the repository owner can grant those rights. Third-party trademarks remain their owners’ property.
