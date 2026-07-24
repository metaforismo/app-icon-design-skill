# Contributing

Keep contributions evidence-led and source-aware.

## Skill changes

- Keep `SKILL.md` under 500 lines.
- Put detailed platform facts in one-level references linked directly from `SKILL.md`.
- Use imperative instructions.
- Update the source snapshot date when changing Apple-specific facts.
- Cite primary Apple documentation for platform behavior.
- Label secondary marketing claims as hypotheses.

## Example assets

- Use original or properly licensed artwork.
- Do not add third-party app icons, Apple templates, hardware replicas, or user-supplied references.
- Include the final prompt and `provenance.yaml`.
- State whether the example is concept-only, static-preflighted, Icon Composer previewed, built, simulated, device-tested, or store-tested.
- Never add a hand-made directory named `.icon`; only Icon Composer creates that file.

## Validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

If Codex’s canonical `skill-creator` is installed, also run:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/design-app-icons
```

