#!/usr/bin/env python3
"""Preflight app-icon bitmaps and generate small-size previews.

This is intentionally a static check. It cannot validate Icon Composer material,
Xcode target selection, system masks, Simulator rendering, or device behavior.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover - exercised in dependency-free use
    raise SystemExit(
        "Pillow is required. Install it in the active environment with "
        "`python -m pip install Pillow`."
    ) from exc


PLATFORM_SPECS = {
    "ios": (1024, 1024),
    "ipados": (1024, 1024),
    "macos": (1024, 1024),
    "visionos": (1024, 1024),
    "watchos": (1088, 1088),
    "tvos": (800, 480),
}

DEFAULT_PREVIEW_SIZES = (16, 20, 29, 40, 60, 76, 83, 128, 256)


@dataclass
class Finding:
    severity: str
    code: str
    message: str


@dataclass
class Audit:
    source: str
    platform: str
    role: str
    width: int
    height: int
    mode: str
    format: str | None
    alpha_present: bool
    alpha_min: int
    alpha_max: int
    nonopaque_pixels: int
    corner_luma_range: float
    edge_luma_range: float
    findings: list[Finding]
    preview_files: list[str]

    @property
    def passed(self) -> bool:
        return not any(item.severity == "error" for item in self.findings)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["passed"] = self.passed
        data["limitations"] = [
            "Static bitmap checks only.",
            "Does not validate Icon Composer material or .icon structure.",
            "Does not validate Xcode target settings, builds, Simulator, devices, App Store, or conversion.",
        ]
        return data


def parse_sizes(value: str) -> tuple[int, ...]:
    try:
        sizes = tuple(sorted({int(item.strip()) for item in value.split(",") if item.strip()}))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("sizes must be comma-separated integers") from exc
    if not sizes or any(size < 8 or size > 1024 for size in sizes):
        raise argparse.ArgumentTypeError("sizes must be between 8 and 1024 pixels")
    return sizes


def alpha_metrics(image: Image.Image) -> tuple[bool, int, int, int]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    minimum, maximum = alpha.getextrema()
    histogram = alpha.histogram()
    nonopaque = sum(histogram[:255])
    return ("A" in image.getbands() or "transparency" in image.info, minimum, maximum, nonopaque)


def luma_range(image: Image.Image, box: tuple[int, int, int, int]) -> float:
    crop = image.convert("L").crop(box)
    minimum, maximum = crop.getextrema()
    return float(maximum - minimum)


def sample_ranges(image: Image.Image) -> tuple[float, float]:
    width, height = image.size
    inset_x = max(1, round(width * 0.05))
    inset_y = max(1, round(height * 0.05))
    corner_boxes = [
        (0, 0, inset_x, inset_y),
        (width - inset_x, 0, width, inset_y),
        (0, height - inset_y, inset_x, height),
        (width - inset_x, height - inset_y, width, height),
    ]
    corner_range = max(luma_range(image, box) for box in corner_boxes)

    edge = max(1, round(min(width, height) * 0.03))
    edge_boxes = [
        (0, 0, width, edge),
        (0, height - edge, width, height),
        (0, 0, edge, height),
        (width - edge, 0, width, height),
    ]
    edge_range = max(luma_range(image, box) for box in edge_boxes)
    return corner_range, edge_range


def checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    width, height = size
    canvas = Image.new("RGB", size, "#f3f4f6")
    draw = ImageDraw.Draw(canvas)
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#d1d5db")
    return canvas


def composite_for_preview(image: Image.Image, size: int) -> Image.Image:
    resized = image.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    background = checkerboard((size, size), max(2, round(size / 8))).convert("RGBA")
    return Image.alpha_composite(background, resized).convert("RGB")


def make_previews(
    image: Image.Image, destination: Path, sizes: Iterable[int], stem: str
) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    previews: list[tuple[int, Image.Image]] = []

    for size in sizes:
        preview = composite_for_preview(image, size)
        path = destination / f"{stem}-{size}px.png"
        preview.save(path, "PNG", optimize=True)
        outputs.append(str(path))
        previews.append((size, preview))

    cell_width = 300
    cell_height = 330
    columns = 3
    rows = math.ceil(len(previews) / columns)
    sheet = Image.new("RGB", (cell_width * columns, cell_height * rows), "#f8fafc")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, (size, preview) in enumerate(previews):
        column = index % columns
        row = index // columns
        x0 = column * cell_width
        y0 = row * cell_height
        scale = min(256 / size, 1)
        shown_size = max(1, round(size * scale))
        shown = preview.resize((shown_size, shown_size), Image.Resampling.NEAREST)
        x = x0 + (cell_width - shown_size) // 2
        y = y0 + 24 + (256 - shown_size) // 2
        sheet.paste(shown, (x, y))
        label = f"{size} × {size}"
        text_box = draw.textbbox((0, 0), label, font=font)
        text_width = text_box[2] - text_box[0]
        draw.text((x0 + (cell_width - text_width) // 2, y0 + 292), label, fill="#111827", font=font)

    sheet_path = destination / f"{stem}-preview-sheet.png"
    sheet.save(sheet_path, "PNG", optimize=True)
    outputs.append(str(sheet_path))
    return outputs


def audit_image(
    source: Path,
    platform: str,
    role: str,
    allow_nonstandard: bool,
    preview_dir: Path | None,
    sizes: tuple[int, ...],
) -> Audit:
    with Image.open(source) as opened:
        source_format = opened.format
        image = opened.copy()

    width, height = image.size
    alpha_present, alpha_min, alpha_max, nonopaque_pixels = alpha_metrics(image)
    corner_range, edge_range = sample_ranges(image)
    findings: list[Finding] = []
    expected = PLATFORM_SPECS[platform]

    if (width, height) != expected:
        severity = "warning" if allow_nonstandard else "error"
        findings.append(
            Finding(
                severity,
                "dimensions",
                f"{platform} expects {expected[0]}×{expected[1]} for this preflight; "
                f"found {width}×{height}. Re-check the exact delivery path in current Apple docs.",
            )
        )

    if role in {"flattened", "concept"} and nonopaque_pixels:
        findings.append(
            Finding(
                "error" if role == "flattened" else "warning",
                "alpha",
                f"Found {nonopaque_pixels} non-opaque pixels. Flattened iOS masters should be "
                "opaque; concept art may retain alpha only when the handoff says so.",
            )
        )

    if role == "layer" and not alpha_present:
        findings.append(
            Finding(
                "warning",
                "layer-alpha",
                "The layer has no alpha channel. This can be valid for a full-canvas layer, "
                "but confirm that it is intentionally opaque.",
            )
        )

    if width == height and role in {"flattened", "concept"} and corner_range > 24:
        findings.append(
            Finding(
                "warning",
                "corner-detail",
                "The outer 5% corners contain visible luminance variation. Confirm that the "
                "artwork is not pre-masked and that corner detail is intended to bleed under the system mask.",
            )
        )

    if edge_range > 160:
        findings.append(
            Finding(
                "warning",
                "edge-complexity",
                "Very high edge contrast was detected near the canvas boundary. Inspect for "
                "mask-aligned borders, clipped focal content, or a surrounding mockup frame.",
            )
        )

    if min(width, height) < 256:
        findings.append(
            Finding(
                "warning",
                "source-size",
                "The source is smaller than 256 px on one edge; use a full-size source for delivery.",
            )
        )

    if not findings:
        findings.append(
            Finding(
                "info",
                "static-preflight",
                "Dimensions and alpha checks passed. Continue with visual, mask, appearance, Xcode, "
                "Simulator, and device validation.",
            )
        )

    preview_files: list[str] = []
    if preview_dir:
        preview_files = make_previews(image, preview_dir, sizes, source.stem)

    return Audit(
        source=str(source),
        platform=platform,
        role=role,
        width=width,
        height=height,
        mode=image.mode,
        format=source_format,
        alpha_present=alpha_present,
        alpha_min=alpha_min,
        alpha_max=alpha_max,
        nonopaque_pixels=nonopaque_pixels,
        corner_luma_range=corner_range,
        edge_luma_range=edge_range,
        findings=findings,
        preview_files=preview_files,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preflight an app-icon bitmap and optionally create small-size previews."
    )
    parser.add_argument("source", type=Path, help="PNG, JPEG, or other Pillow-readable image")
    parser.add_argument("--platform", choices=sorted(PLATFORM_SPECS), default="ios")
    parser.add_argument("--role", choices=("concept", "flattened", "layer"), default="flattened")
    parser.add_argument(
        "--allow-nonstandard",
        action="store_true",
        help="Downgrade a platform-dimension mismatch from error to warning",
    )
    parser.add_argument("--preview-dir", type=Path, help="Directory for resized previews and sheet")
    parser.add_argument(
        "--sizes",
        type=parse_sizes,
        default=DEFAULT_PREVIEW_SIZES,
        help="Comma-separated square preview sizes",
    )
    parser.add_argument("--report", type=Path, help="Write the JSON audit to this path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.source.is_file():
        print(f"error: source not found: {args.source}", file=sys.stderr)
        return 2

    audit = audit_image(
        args.source,
        args.platform,
        args.role,
        args.allow_nonstandard,
        args.preview_dir,
        args.sizes,
    )
    payload = audit.to_dict()
    output = json.dumps(payload, indent=2)
    print(output)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")

    return 0 if audit.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
