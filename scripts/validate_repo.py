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

    script = SKILL / "scripts" / "icon_qa.py"
    if not script.is_file():
        result.error("Missing icon_qa.py")


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


def validate_repo_hygiene(result: Result) -> None:
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "NOTICE.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / ".github" / "workflows" / "validate.yml",
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
    text_extensions = {".md", ".yaml", ".yml", ".py", ".txt", ".json"}
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
