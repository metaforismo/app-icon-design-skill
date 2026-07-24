#!/usr/bin/env python3
"""Build a deterministic installable skill archive and SHA-256 manifest."""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "design-app-icons"
DIST = ROOT / "dist"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ARCHIVE = DIST / f"design-app-icons-v{VERSION}.zip"
CHECKSUMS = DIST / "SHA256SUMS.txt"
ZIP_TIMESTAMP = (2026, 7, 24, 0, 0, 0)


def iter_skill_files() -> list[Path]:
    return sorted(
        path
        for path in SKILL.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )


def build_archive() -> Path:
    DIST.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in iter_skill_files():
            relative = Path("design-app-icons") / path.relative_to(SKILL)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if path.parent.name == "scripts" and path.suffix == ".py" else 0o644
            info.external_attr = (mode & 0xFFFF) << 16
            bundle.writestr(info, path.read_bytes())
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    CHECKSUMS.write_text(f"{digest}  {ARCHIVE.name}\n", encoding="utf-8")
    return ARCHIVE


def main() -> int:
    archive = build_archive()
    print(archive)
    print(CHECKSUMS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
