#!/usr/bin/env python3
"""Validate repository structure, skill metadata, references, and examples."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "design-app-icons"
SKILL_MD = SKILL / "SKILL.md"


@dataclass
class Result:
    errors: list[str]
    warnings: list[str]

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def split_frontmatter(text: str, result: Result) -> tuple[dict, str]:
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.DOTALL)
    if not match:
        result.error("SKILL.md must start with YAML frontmatter delimited by ---")
        return {}, text
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        result.error(f"SKILL.md frontmatter is invalid YAML: {exc}")
        return {}, match.group(2)
    if not isinstance(metadata, dict):
        result.error("SKILL.md frontmatter must be a mapping")
        return {}, match.group(2)
    return metadata, match.group(2)


def validate_skill(result: Result) -> None:
    if not SKILL_MD.is_file():
        result.error("Missing skills/design-app-icons/SKILL.md")
        return

    text = SKILL_MD.read_text(encoding="utf-8")
    metadata, body = split_frontmatter(text, result)
    if set(metadata) != {"name", "description"}:
        result.error("SKILL.md frontmatter must contain only name and description")
    if metadata.get("name") != "design-app-icons":
        result.error("SKILL.md name must be design-app-icons")
    description = metadata.get("description")
    if not isinstance(description, str) or len(description.strip()) < 80:
        result.error("SKILL.md description must be a comprehensive trigger description")
    if len(text.splitlines()) >= 500:
        result.error("SKILL.md must remain under 500 lines")
    if "TODO" in text:
        result.error("SKILL.md contains TODO")

    linked = set(re.findall(r"\]\((references/[^)]+\.md)\)", body))
    actual = {
        str(path.relative_to(SKILL))
        for path in (SKILL / "references").glob("*.md")
        if path.is_file()
    }
    for relative in sorted(linked):
        if not (SKILL / relative).is_file():
            result.error(f"SKILL.md links missing reference: {relative}")
    for relative in sorted(actual - linked):
        result.error(f"Reference is not directly linked from SKILL.md: {relative}")

    for script_name in ("icon_qa.py", "prepare_raster_layer.py", "compose_raster_layers.py"):
        script = SKILL / "scripts" / script_name
        if not script.is_file():
            result.error(f"Missing {script_name}")
    if not (SKILL / "assets" / "layer-composition-template.yaml").is_file():
        result.error("Missing layer-composition-template.yaml")


def validate_agent_metadata(result: Result) -> None:
    path = SKILL / "agents" / "openai.yaml"
    if not path.is_file():
        result.error("Missing agents/openai.yaml")
        return
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    interface = data.get("interface", {}) if isinstance(data, dict) else {}
    required = {"display_name", "short_description", "default_prompt"}
    if set(interface) != required:
        result.error("agents/openai.yaml interface must contain the three generated fields only")
    short = interface.get("short_description", "")
    if not 25 <= len(short) <= 64:
        result.error("short_description must be 25-64 characters")
    if "$design-app-icons" not in interface.get("default_prompt", ""):
        result.error("default_prompt must mention $design-app-icons")


def validate_examples(result: Result) -> None:
    examples = ROOT / "examples"
    expected = {"quiet-tide", "parcel-pulse", "mood-lantern", "orbit-stack"}
    actual = {path.name for path in examples.iterdir() if path.is_dir()}
    if actual != expected:
        result.error(f"Expected example directories {sorted(expected)}, found {sorted(actual)}")

    for name in sorted(expected):
        directory = examples / name
        for filename in ("concept-master.png", "prompt.md", "case-study.md", "provenance.yaml"):
            if not (directory / filename).is_file():
                result.error(f"{name} is missing {filename}")

        image_path = directory / "concept-master.png"
        if image_path.is_file():
            with Image.open(image_path) as image:
                if image.size != (1024, 1024):
                    result.error(f"{name} concept must be 1024×1024, found {image.size}")
                rgba = image.convert("RGBA")
                minimum, maximum = rgba.getchannel("A").getextrema()
                if (minimum, maximum) != (255, 255):
                    result.error(f"{name} concept must be opaque")

        provenance_path = directory / "provenance.yaml"
        if provenance_path.is_file():
            provenance = yaml.safe_load(provenance_path.read_text(encoding="utf-8"))
            required = {
                "name",
                "generated_at",
                "tool_mode",
                "prompt_file",
                "input_roles",
                "rights_note",
                "status",
            }
            if set(provenance) != required:
                result.error(f"{name} provenance keys do not match the required schema")
            if provenance.get("tool_mode") != "built-in image_gen":
                result.error(f"{name} must record the built-in image_gen mode")
            status = provenance.get("status", "")
            if "not an Icon Composer file" not in status:
                result.error(f"{name} must retain the concept-only evidence boundary")

    quiet_tide = examples / "quiet-tide"
    production_files = (
        quiet_tide / "layers" / "01-backdrop.svg",
        quiet_tide / "layers" / "02-sun.svg",
        quiet_tide / "layers" / "03-wave.svg",
        quiet_tide / "production" / "QuietTide.icon" / "icon.json",
        quiet_tide / "production" / "README.md",
        quiet_tide / "production" / "evidence.md",
        quiet_tide / "production" / "fixture" / "project.yml",
        quiet_tide / "production" / "fixture" / "Sources" / "QuietTideFixtureApp.swift",
        quiet_tide / "production" / "evidence" / "composer-default.png",
        quiet_tide / "production" / "evidence" / "composer-dark.png",
        quiet_tide / "production" / "evidence" / "composer-mono.png",
        quiet_tide / "production" / "evidence" / "composer-watchos-default.png",
        quiet_tide / "production" / "evidence" / "export-default.png",
        quiet_tide / "production" / "evidence" / "simulator-home.png",
    )
    for path in production_files:
        if not path.is_file():
            result.error(f"Quiet Tide production evidence is missing {path.relative_to(quiet_tide)}")

    icon_json = quiet_tide / "production" / "QuietTide.icon" / "icon.json"
    if icon_json.is_file():
        data = yaml.safe_load(icon_json.read_text(encoding="utf-8"))
        groups = data.get("groups", []) if isinstance(data, dict) else []
        layer_names = {
            layer.get("image-name")
            for group in groups
            for layer in group.get("layers", [])
            if isinstance(layer, dict)
        }
        if layer_names != {"01-backdrop.svg", "02-sun.svg", "03-wave.svg"}:
            result.error("QuietTide.icon must contain the three expected SVG layers")

    mood_layers = examples / "mood-lantern" / "layer-first"
    for relative in (
        "README.md",
        "prompts.md",
        "raw/01-backdrop.png",
        "raw/02-lantern-shell.png",
        "raw/03-amber-glow.png",
        "raw/02-lantern-shell-key.png",
        "raw/03-amber-glow-key.png",
        "candidate/01-backdrop.png",
        "candidate/02-amber-glow.png",
        "candidate/03-lantern-shell.png",
        "assembled-proof.png",
        "qa/glow-cleanup.json",
        "qa/shell-cleanup.json",
        "qa/glow-audit.json",
        "qa/shell-audit.json",
        "qa/static-audit.json",
        "qa/previews/assembled-proof-ios-appearance-sheet.png",
    ):
        if not (mood_layers / relative).is_file():
            result.error(f"Mood Lantern layer-first evidence is missing {relative}")

    for relative in ("candidate/02-amber-glow.png", "candidate/03-lantern-shell.png"):
        with Image.open(mood_layers / relative) as image:
            if image.size != (1024, 1024) or image.mode != "RGBA":
                result.error(f"Mood Lantern {relative} must be a 1024x1024 RGBA layer")

    with Image.open(mood_layers / "assembled-proof.png") as image:
        if image.size != (1024, 1024) or image.mode != "RGB":
            result.error("Mood Lantern assembled proof must be an opaque 1024x1024 RGB PNG")


def validate_repo_hygiene(result: Result) -> None:
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "NOTICE.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CHANGELOG.md",
        ROOT / "VERSION",
        ROOT / ".github" / "workflows" / "validate.yml",
        ROOT / ".github" / "workflows" / "source-freshness.yml",
        ROOT / "docs" / "source-manifest.yaml",
        ROOT / "scripts" / "check_sources.py",
        ROOT / "scripts" / "install.sh",
        ROOT / "scripts" / "package_skill.py",
        ROOT / "assets" / "social-preview.png",
        ROOT / "assets" / "social-preview-prompt.md",
        ROOT / "experiments" / "quiet-tide-ppo" / "experiment.yaml",
        ROOT / "experiments" / "quiet-tide-ppo" / "result-template.md",
    ]
    for path in required:
        if not path.is_file():
            result.error(f"Missing repository file: {path.relative_to(ROOT)}")

    # Assemble these values so the validator does not flag its own source while
    # still rejecting leaked attachment and temporary paths elsewhere.
    forbidden_patterns = (
        "codex" + "-clipboard-",
        "/var/" + "folders/",
        ".codex/" + "attachments/",
    )
    unresolved_template_marker = "[" + "TODO"
    text_extensions = {".md", ".yaml", ".yml", ".py", ".txt", ".json", ".swift", ".svg"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_extensions:
            continue
        content = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if pattern in content:
                result.error(f"{path.relative_to(ROOT)} leaks a private reference path: {pattern}")
        if unresolved_template_marker in content:
            result.error(f"{path.relative_to(ROOT)} contains unresolved template text")


def run() -> Result:
    result = Result(errors=[], warnings=[])
    validate_skill(result)
    validate_agent_metadata(result)
    validate_examples(result)
    validate_repo_hygiene(result)
    return result


def main() -> int:
    result = run()
    for warning in result.warnings:
        print(f"warning: {warning}")
    for error in result.errors:
        print(f"error: {error}")
    if result.errors:
        print(f"FAILED: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
        return 1
    print(f"PASS: repository validation succeeded with {len(result.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
