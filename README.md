# App Icon Studio

[![Validate](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/validate.yml)
[![Source freshness](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/source-freshness.yml/badge.svg)](https://github.com/metaforismo/app-icon-design-skill/actions/workflows/source-freshness.yml)

![App Icon Studio identity](assets/social-preview.png)

`$design-app-icons` is an iOS-first Codex skill that separates fast visual exploration from deliberate Apple production. It uses built-in Imagegen for complete icon concepts, pauses for explicit approval, then reconstructs the chosen design and finishes compatible shipping icons in Apple Icon Composer.

## The workflow

```text
Brief → category collision scan → 1–2 complete icon directions
      → versioned, one-variable revisions → explicit visual approval
      → Composer-feasibility gate → deliberate SVG/PNG sources
      → Icon Composer → Xcode, small-size, and real-context validation
```

Concept work stays simple: one complete icon per generation, one or two directions rather than an automatic three, stable version IDs, and one focused change per revision. No exploded diagrams or production layers appear before approval.

For a shipping iPhone, iPad, Mac, or Apple Watch icon, Icon Composer is the planned final route. If translation would visibly change the approved identity, the skill returns with a named Composer-adapted concept for approval. A complex illustrative icon can use a flattened fallback only when the user chooses fidelity over adaptation; the handoff then states that Composer was not used.

tvOS and visionOS remain Xcode asset-catalog workflows.

## What a session feels like

```text
User: Create an icon for a calm private journal.

Studio: Here are A1 and B1. Each is a complete icon, shown full-size and
at 32 px. A1 uses a folded page; B1 uses a quiet tide. Which direction
should I revise?

User: B1, but make the sun smaller.

Studio: B2 changes only the sun scale. The wave, palette, lighting,
composition, and silhouette remain locked. Revise one element, or say
"I approve B2."

User: I approve B2.

Studio: Visual approval recorded. I will now reconstruct the minimum
source roles, compare the proof with B2, author the .icon in Icon Composer,
and validate Xcode and requested runtime contexts. If fidelity requires a
visible change, I will return with a new version for approval.
```

Visual approval and technical validation are different gates. A valid file is not automatically a good icon, and an attractive bitmap is not automatically a valid `.icon`.

## Icon Composer model

The skill follows Apple’s current authoring model:

- SVG or PNG artwork on the current 1024 × 1024 or 1088 × 1088 canvas;
- no source mask, baked specular, refraction, inter-group shadow, or simple background fill;
- no more than four semantic depth groups;
- Individual or Combined group material behavior;
- restrained specular, refraction, blur, translucency, and shadow;
- Default, Dark, and Mono authoring, with Clear/Tinted light/dark previews from Mono;
- platform-specific composition overrides only when optical balance requires them;
- a real tool-saved `.icon` associated with the Xcode target.

See the detailed [Icon Composer production workflow](skills/design-app-icons/references/liquid-glass-icon-composer.md).

## Install

```bash
git clone --depth 1 --branch v2.0.0 https://github.com/metaforismo/app-icon-design-skill.git
cd app-icon-design-skill
./scripts/install.sh
```

Or copy the installable folder:

```bash
cp -R skills/design-app-icons "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Invoke it explicitly:

```text
Use $design-app-icons to design and ship an original iOS icon for my private journal. Show at most two complete directions, iterate until I explicitly approve one, then finish it in Icon Composer and validate it in Xcode.
```

Other useful requests:

- “Create one complete direction from this precise brief and wait for approval.”
- “Edit B2 but change only the palette.”
- “Audit this icon at 16–256 px and in realistic contexts.”
- “I approve B3. Reconstruct it faithfully and continue through Icon Composer.”
- “Assess whether this approved illustration needs a Composer-adapted version.”
- “Audit an existing `.icon` across appearances, backgrounds, and lighting angles.”

## Included

- installable [`design-app-icons` skill](skills/design-app-icons/SKILL.md);
- current Apple platform, Icon Composer, Liquid Glass, Imagegen, QA, and delivery references;
- deterministic [`icon_qa.py`](skills/design-app-icons/scripts/icon_qa.py) preflight with small-size, appearance, and synthetic context boards;
- templates for briefs, version cards, approval locks, layer contracts, and evidence reports;
- four fictional, original concept studies;
- a tool-authored Quiet Tide `.icon` and Xcode/Simulator fixture demonstrating one validated geometric reconstruction.

The example artwork teaches constraints and evidence boundaries; it is not the skill’s identity. The existing App Icon Studio identity remains unchanged in this release. Future generated repository branding must pass the same named-version approval gate before publication.

## Static preflight

```bash
python3 skills/design-app-icons/scripts/icon_qa.py path/to/icon.png \
  --platform ios \
  --role flattened \
  --preview-dir work/icon-previews \
  --report work/icon-audit.json
```

The CLI checks dimensions, format, alpha, edge behavior, color-profile presence, and produces small-size, heuristic appearance, and synthetic context previews. It does not reproduce Apple rendering or validate Composer, Xcode selection, Simulator, hardware, App Review, or conversion.

## Validate

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

- **Validated:** directly observed tests, artifacts, commands, versions, or screenshots.
- **Prepared:** files exist but still require the named import, build, runtime, device, or store step.
- **Not tested:** every Composer, Xcode, Simulator, device, older-release fallback, App Review, or conversion outcome not actually observed.

Current claims are grounded in Apple’s official documentation and recorded in the [source ledger](skills/design-app-icons/references/sources.md). The supplied third-party screenshots are not redistributed. No workflow guarantees App Review approval, ranking, or conversion improvement.

See the [implementation and per-icon checklist](TODO.md), [changelog](CHANGELOG.md), [research notes](docs/research-notes.md), and [contribution guide](CONTRIBUTING.md). Repository-owned code, documentation, and original examples are available under the [MIT License](LICENSE), to the extent the owner can grant those rights.
