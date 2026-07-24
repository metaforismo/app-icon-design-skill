# App Icon Studio

[![Validate](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/validate.yml)
[![Source freshness](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/source-freshness.yml/badge.svg)](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/source-freshness.yml)

![App Icon Studio identity](assets/social-preview.png)

`$design-app-icons` is a Codex skill for creating, revising, and validating original app icons. It is iOS-first, uses the built-in Imagegen workflow, and treats the approved whole image as the default final artwork.

## The default flow

```text
Brief → whole-icon directions → targeted revisions → explicit approval
      → final 1024 × 1024 image → small-size and static QA → stop
```

The skill generates one complete icon at a time. It keeps the selected version stable, applies focused revisions, and waits for the user to explicitly approve a named image.

After approval, it preserves that image and stops after export and QA. It does not automatically generate components, reconstruct SVGs, open Icon Composer, or modify Xcode.

Optional production work begins only when the user asks for it:

- integrate the approved flattened artwork into an app project;
- reconstruct simple, deliberate editable geometry;
- prepare minimal Icon Composer sources when separation preserves the design;
- audit an existing icon, alternate icon, or App Store experiment.

If an editable reconstruction changes the silhouette, proportions, lighting, glow, material continuity, or recognition anchor, the reconstruction is rejected and the approved image remains authoritative.

## Install

```bash
git clone --depth 1 --branch v1.3.0 https://github.com/metaforismo/app-icon-design-skill.git
cd app-icon-design-skill
./scripts/install.sh
```

Or copy the installable folder:

```bash
cp -R skills/design-app-icons "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Invoke it explicitly:

```text
Use $design-app-icons to create three original whole-icon directions for a private journaling app. Iterate on my selected direction until I explicitly approve it, then export and audit the final image.
```

Other useful requests:

- “Audit this iOS icon at 16–256 px and prioritize the problems.”
- “Edit this selected concept but change only the palette.”
- “I approve version B3. Finalize the image, audit it, and stop.”
- “Integrate this approved flattened icon into my Xcode project.”
- “Assess whether this approved geometric design can survive Icon Composer separation.”
- “Design three Product Page Optimization icon hypotheses without promising conversion lift.”

## What is included

- the installable [`design-app-icons` skill](skills/design-app-icons/SKILL.md);
- focused references for Apple platforms, Icon Composer, Liquid Glass, Imagegen, QA, delivery, and App Store experimentation;
- a deterministic [`icon_qa.py`](skills/design-app-icons/scripts/icon_qa.py) preflight CLI;
- four fictional, original concept studies: [Quiet Tide](examples/quiet-tide/case-study.md), [Parcel Pulse](examples/parcel-pulse/case-study.md), [Mood Lantern](examples/mood-lantern/case-study.md), and [Orbit Stack](examples/orbit-stack/case-study.md);
- an optional, tool-authored Quiet Tide Icon Composer/Xcode/Simulator fixture for advanced delivery evidence.

The examples are learning material, not the identity of the skill. The App Icon Studio identity is the folded ribbon mark shown above.

## Static preflight

```bash
python3 skills/design-app-icons/scripts/icon_qa.py path/to/icon.png \
  --platform ios \
  --role flattened \
  --preview-dir work/icon-previews \
  --report work/icon-audit.json
```

The CLI checks dimensions, format, alpha and edge behavior, color-profile presence, and small-size previews. Its masks and appearance transforms are heuristic stress tests. It does not validate Icon Composer material, Xcode target selection, Simulator, hardware, App Review, or conversion.

## Validate the repository

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/design-app-icons
python3 scripts/package_skill.py
```

## Evidence boundaries

- **Validated:** repository tests, canonical skill structure, static audits, and the checked-in Quiet Tide evidence explicitly labeled as validated.
- **Prepared:** source files that exist but still require platform import or build.
- **Not tested:** any Icon Composer, Xcode, Simulator, device, App Review, or conversion outcome not backed by named evidence.

Current platform claims are grounded in Apple’s official documentation and recorded in the [source ledger](skills/design-app-icons/references/sources.md). The supplied third-party screenshots are not redistributed. Following the workflow does not guarantee App Review approval, ranking, or conversion improvement.

See the [changelog](CHANGELOG.md), [research notes](docs/research-notes.md), and [contribution guide](CONTRIBUTING.md). Code, documentation, and repository-owned example assets are available under the [MIT License](LICENSE), to the extent the repository owner can grant those rights.
