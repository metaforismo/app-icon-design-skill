#!/usr/bin/env python3
"""Preflight app-icon bitmaps and generate platform-aware previews.

The masks and appearance simulations in this script are review heuristics. They
do not reproduce Apple's rendering pipeline and cannot validate Icon Composer,
Xcode target selection, Simulator rendering, device behavior, or App Store use.
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
    from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install it in the active environment with "
        "`python3 -m pip install Pillow`."
    ) from exc


PLATFORM_SPECS = {
    "ios": (1024, 1024),
    "ipados": (1024, 1024),
    "macos": (1024, 1024),
    "visionos": (1024, 1024),
    "watchos": (1088, 1088),
    "tvos": (800, 480),
}

PLATFORM_MASKS = {
    "ios": "rounded-rectangle",
    "ipados": "rounded-rectangle",
    "macos": "rounded-rectangle",
    "visionos": "circle",
    "watchos": "circle",
    "tvos": "rounded-rectangle",
}

DEFAULT_PREVIEW_SIZES = (16, 20, 29, 40, 60, 76, 83, 128, 256)
APPEARANCES = ("light", "dark", "mono", "tinted")
SUPPORTED_FORMATS = {"PNG", "JPEG"}


def ui_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


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
    icc_profile_present: bool
    alpha_present: bool
    alpha_min: int
    alpha_max: int
    nonopaque_pixels: int
    alpha_content_box: tuple[int, int, int, int] | None
    corner_alpha_max: int
    corner_luma_range: float
    edge_luma_range: float
    preview_mask: str
    findings: list[Finding]
    preview_files: list[str]

    @property
    def passed(self) -> bool:
        return not any(item.severity == "error" for item in self.findings)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["passed"] = self.passed
        data["limitations"] = [
            "Static bitmap checks and approximate context previews only.",
            "Preview masks are heuristics, not Apple's official mask geometry.",
            "Mono and tinted previews are simulations, not Icon Composer renders.",
            "Does not validate .icon structure, Xcode settings/builds, Simulator, device, App Store, or conversion.",
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


def parse_box(value: str) -> tuple[int, int, int, int]:
    try:
        box = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box must contain comma-separated integers") from exc
    if len(box) != 4 or box[2] <= box[0] or box[3] <= box[1]:
        raise argparse.ArgumentTypeError("box must be left,top,right,bottom")
    return box


def alpha_metrics(image: Image.Image) -> tuple[bool, int, int, int]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    minimum, maximum = alpha.getextrema()
    histogram = alpha.histogram()
    nonopaque = sum(histogram[:255])
    return ("A" in image.getbands() or "transparency" in image.info, minimum, maximum, nonopaque)


def alpha_geometry(image: Image.Image) -> tuple[tuple[int, int, int, int] | None, int]:
    alpha = image.convert("RGBA").getchannel("A")
    width, height = image.size
    corners = (
        alpha.getpixel((0, 0)),
        alpha.getpixel((width - 1, 0)),
        alpha.getpixel((0, height - 1)),
        alpha.getpixel((width - 1, height - 1)),
    )
    return alpha.getbbox(), max(corners)


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
    return corner_range, max(luma_range(image, box) for box in edge_boxes)


def checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    width, height = size
    canvas = Image.new("RGB", size, "#f3f4f6")
    draw = ImageDraw.Draw(canvas)
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#d1d5db")
    return canvas


def preview_dimensions(size: int, platform: str) -> tuple[int, int]:
    expected_width, expected_height = PLATFORM_SPECS[platform]
    return size, max(1, round(size * expected_height / expected_width))


def platform_mask(size: tuple[int, int], platform: str) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    if PLATFORM_MASKS[platform] == "circle":
        draw.ellipse((0, 0, width - 1, height - 1), fill=255)
    else:
        radius_ratio = 0.12 if platform == "tvos" else 0.22
        draw.rounded_rectangle(
            (0, 0, width - 1, height - 1),
            radius=max(1, round(min(width, height) * radius_ratio)),
            fill=255,
        )
    return mask


def fit_without_distortion(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    fitted = ImageOps.contain(image.convert("RGBA"), size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    offset = ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2)
    canvas.alpha_composite(fitted, offset)
    return canvas


def appearance_art(image: Image.Image, appearance: str) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if appearance in {"light", "dark"}:
        return rgba
    gray = ImageOps.grayscale(rgba)
    if appearance == "mono":
        color = ImageOps.colorize(gray, black="#2b2d31", white="#f7f7f8")
    else:
        color = ImageOps.colorize(gray, black="#163d38", white="#8ff5de")
    color.putalpha(alpha)
    return color


def render_context_preview(
    image: Image.Image, size: int, platform: str, appearance: str = "light"
) -> Image.Image:
    dimensions = preview_dimensions(size, platform)
    art = appearance_art(fit_without_distortion(image, dimensions), appearance)
    alpha = ImageChops.multiply(art.getchannel("A"), platform_mask(dimensions, platform))
    art.putalpha(alpha)
    if appearance == "dark":
        background = Image.new("RGBA", dimensions, "#111318")
    elif appearance == "tinted":
        background = Image.new("RGBA", dimensions, "#d8f4ed")
    elif appearance == "mono":
        background = Image.new("RGBA", dimensions, "#8b8c90")
    else:
        background = checkerboard(dimensions, max(2, round(min(dimensions) / 8))).convert("RGBA")
    return Image.alpha_composite(background, art).convert("RGB")


def composite_for_preview(image: Image.Image, size: int, platform: str = "ios") -> Image.Image:
    """Backwards-compatible default preview helper."""
    return render_context_preview(image, size, platform, "light")


def make_previews(
    image: Image.Image,
    destination: Path,
    sizes: Iterable[int],
    stem: str,
    platform: str = "ios",
) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    sizes = tuple(sizes)

    for size in sizes:
        preview = render_context_preview(image, size, platform, "light")
        width, height = preview.size
        path = destination / f"{stem}-{width}x{height}px.png"
        preview.save(path, "PNG", optimize=True)
        outputs.append(str(path))

    cell_width, cell_height = 286, 320
    sheet = Image.new("RGB", (cell_width * len(APPEARANCES), cell_height * len(sizes)), "#eef1f5")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for column, appearance in enumerate(APPEARANCES):
        draw.text((column * cell_width + 18, 12), appearance.title(), fill="#111827", font=font)
    for row, size in enumerate(sizes):
        for column, appearance in enumerate(APPEARANCES):
            preview = render_context_preview(image, size, platform, appearance)
            scale = min(240 / preview.width, 240 / preview.height, 1)
            shown = preview.resize(
                (max(1, round(preview.width * scale)), max(1, round(preview.height * scale))),
                Image.Resampling.NEAREST,
            )
            x0, y0 = column * cell_width, row * cell_height
            x = x0 + (cell_width - shown.width) // 2
            y = y0 + 42 + (240 - shown.height) // 2
            sheet.paste(shown, (x, y))
            label = f"{preview.width} × {preview.height}"
            text_box = draw.textbbox((0, 0), label, font=font)
            draw.text(
                (x0 + (cell_width - (text_box[2] - text_box[0])) // 2, y0 + 292),
                label,
                fill="#111827",
                font=font,
            )

    sheet_path = destination / f"{stem}-{platform}-appearance-sheet.png"
    sheet.save(sheet_path, "PNG", optimize=True)
    outputs.append(str(sheet_path))

    context_path = destination / f"{stem}-{platform}-context-board.png"
    make_context_board(image, platform).save(context_path, "PNG", optimize=True)
    outputs.append(str(context_path))
    return outputs


def masked_icon(image: Image.Image, size: int, platform: str, appearance: str) -> Image.Image:
    dimensions = preview_dimensions(size, platform)
    art = appearance_art(fit_without_distortion(image, dimensions), appearance)
    alpha = ImageChops.multiply(art.getchannel("A"), platform_mask(dimensions, platform))
    art.putalpha(alpha)
    return art


def generic_neighbor(size: int, color: str, shape: str) -> Image.Image:
    tile = Image.new("RGBA", (size, size), color)
    mask = platform_mask((size, size), "ios")
    tile.putalpha(mask)
    draw = ImageDraw.Draw(tile)
    inset = round(size * 0.28)
    box = (inset, inset, size - inset, size - inset)
    if shape == "circle":
        draw.ellipse(box, fill="#ffffffcc")
    elif shape == "diamond":
        middle = size // 2
        draw.polygon(((middle, inset), (size - inset, middle), (middle, size - inset), (inset, middle)), fill="#ffffffcc")
    else:
        draw.rounded_rectangle(box, radius=max(2, size // 12), fill="#ffffffcc")
    return tile


def paste_with_shadow(canvas: Image.Image, icon: Image.Image, position: tuple[int, int]) -> None:
    x, y = position
    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow.putalpha(icon.getchannel("A").point(lambda value: round(value * 0.22)))
    canvas.alpha_composite(shadow, (x, y + max(2, icon.height // 18)))
    canvas.alpha_composite(icon, position)


def make_context_board(image: Image.Image, platform: str = "ios") -> Image.Image:
    """Create a synthetic salience board; this is not a system-rendering simulation."""
    canvas = Image.new("RGBA", (1200, 760), "#eef1f6")
    draw = ImageDraw.Draw(canvas)
    title_font = ui_font(18)
    label_font = ui_font(15)
    body_font = ui_font(16)
    caption_font = ui_font(13)
    draw.text((28, 18), "Synthetic context board — heuristic, not an Apple render", fill="#111827", font=title_font)

    panels = (
        (24, 56, 576, 406, "Light wallpaper", "#dcecff", "light"),
        (600, 56, 1176, 406, "Dark wallpaper", "#171b2b", "dark"),
    )
    colors = ("#ef665b", "#3d7cff", "#1eb980", "#8b5cf6", "#f2a93b", "#475569", "#dc4f91")
    shapes = ("circle", "diamond", "square")
    for left, top, right, bottom, label, background, appearance in panels:
        draw.rounded_rectangle((left, top, right, bottom), radius=28, fill=background)
        label_color = "#111827" if appearance == "light" else "#f8fafc"
        draw.text((left + 22, top + 18), label, fill=label_color, font=label_font)
        icon_size = 88
        gap_x, gap_y = 124, 132
        target_index = 2
        for index in range(8):
            row, column = divmod(index, 4)
            x = left + 50 + column * gap_x
            y = top + 66 + row * gap_y
            if index == target_index:
                icon = masked_icon(image, icon_size, platform, appearance)
                paste_with_shadow(canvas, icon, (x, y))
                badge_radius = 15
                badge_x, badge_y = x + icon.width - 5, y + 5
                draw.ellipse((badge_x - badge_radius, badge_y - badge_radius, badge_x + badge_radius, badge_y + badge_radius), fill="#ff3b30", outline="#ffffff", width=3)
            else:
                icon = generic_neighbor(icon_size, colors[index % len(colors)], shapes[index % len(shapes)])
                paste_with_shadow(canvas, icon, (x, y))

    draw.rounded_rectangle((24, 430, 1176, 736), radius=28, fill="#ffffff")
    draw.text((48, 450), "Search and Settings scale", fill="#111827", font=label_font)
    rows = ((500, 64, "Search result — 64 px"), (620, 40, "Settings row — 40 px"))
    for y, size, label in rows:
        draw.rounded_rectangle((48, y - 18, 1152, y + max(86, size + 28)), radius=18, fill="#f5f7fa")
        icon = masked_icon(image, size, platform, "light")
        paste_with_shadow(canvas, icon, (76, y))
        draw.text((76 + max(icon.width, size) + 28, y + 5), label, fill="#111827", font=body_font)
        draw.text((76 + max(icon.width, size) + 28, y + 34), "Does the recognition anchor survive without texture or micro-detail?", fill="#52606d", font=caption_font)
    return canvas.convert("RGB")


def audit_image(
    source: Path,
    platform: str,
    role: str,
    allow_nonstandard: bool,
    preview_dir: Path | None,
    sizes: tuple[int, ...],
    expected_content_box: tuple[int, int, int, int] | None = None,
) -> Audit:
    with Image.open(source) as opened:
        source_format = opened.format
        icc_profile_present = bool(opened.info.get("icc_profile"))
        image = opened.copy()

    width, height = image.size
    alpha_present, alpha_min, alpha_max, nonopaque_pixels = alpha_metrics(image)
    alpha_content_box, corner_alpha_max = alpha_geometry(image)
    corner_range, edge_range = sample_ranges(image)
    findings: list[Finding] = []
    expected = PLATFORM_SPECS[platform]

    if source_format not in SUPPORTED_FORMATS:
        findings.append(Finding("warning", "format", f"{source_format or 'Unknown'} is readable, but PNG or JPEG is safer for this static audit."))
    if role in {"flattened", "layer"} and source_format != "PNG":
        findings.append(Finding("warning", "delivery-format", "Use PNG for deterministic flattened or transparent-layer delivery unless the target workflow explicitly accepts another format."))
    if not icc_profile_present:
        findings.append(Finding("warning", "icc-profile", "No embedded ICC profile was detected. Confirm sRGB, Display P3, or Gray Gamma 2.2 in the production source."))

    if (width, height) != expected:
        severity = "warning" if allow_nonstandard else "error"
        findings.append(Finding(severity, "dimensions", f"{platform} expects {expected[0]}×{expected[1]} for this preflight; found {width}×{height}. Re-check the exact delivery path in current Apple docs."))
    if role in {"flattened", "concept"} and nonopaque_pixels:
        findings.append(Finding("error" if role == "flattened" else "warning", "alpha", f"Found {nonopaque_pixels} non-opaque pixels. Flattened iOS masters should be opaque; concept art may retain alpha only when the handoff says so."))
    if role == "layer" and not alpha_present:
        findings.append(Finding("error", "layer-alpha", "The foreground layer has no alpha channel. A visible checkerboard may be baked into opaque RGB pixels; use role=flattened for an intentionally opaque full-canvas layer."))
    if role == "layer" and alpha_present and alpha_min != 0:
        findings.append(Finding("error", "layer-transparency", "The foreground layer has no fully transparent pixels. Confirm the matte and reject opaque presentation canvases."))
    if role == "layer" and alpha_present and corner_alpha_max != 0:
        findings.append(Finding("error", "layer-corners", f"At least one canvas corner has alpha {corner_alpha_max}; foreground-layer corners must be fully transparent."))
    if role == "layer" and alpha_present and alpha_max < 255:
        findings.append(Finding("warning", "layer-opacity", "The layer never reaches full opacity. Confirm that all-over translucency is intrinsic artwork rather than an accidental matte."))
    if role == "layer" and alpha_content_box is None:
        findings.append(Finding("error", "empty-layer", "The layer contains no visible alpha content."))
    if expected_content_box and alpha_content_box:
        left, top, right, bottom = alpha_content_box
        expected_left, expected_top, expected_right, expected_bottom = expected_content_box
        if left < expected_left or top < expected_top or right > expected_right or bottom > expected_bottom:
            findings.append(Finding("error", "content-box", f"Alpha content {alpha_content_box} extends outside expected box {expected_content_box}."))
    if width == height and role in {"flattened", "concept"} and corner_range > 24:
        findings.append(Finding("warning", "corner-detail", "The outer 5% corners contain visible luminance variation. Confirm the artwork is not pre-masked and corner detail is intended to bleed under the system mask."))
    if edge_range > 160:
        findings.append(Finding("warning", "edge-complexity", "Very high edge contrast was detected near the canvas boundary. Inspect for mask-aligned borders, clipped focal content, or a mockup frame."))
    if min(width, height) < 256:
        findings.append(Finding("warning", "source-size", "The source is smaller than 256 px on one edge; use a full-size source for delivery."))
    if not any(item.severity in {"error", "warning"} for item in findings):
        findings.append(Finding("info", "static-preflight", "Dimensions, format, profile, and alpha checks passed. Continue with visual, official-mask, Icon Composer, Xcode, Simulator, and device validation."))

    preview_files = make_previews(image, preview_dir, sizes, source.stem, platform) if preview_dir else []
    return Audit(
        source=str(source), platform=platform, role=role, width=width, height=height,
        mode=image.mode, format=source_format, icc_profile_present=icc_profile_present,
        alpha_present=alpha_present, alpha_min=alpha_min, alpha_max=alpha_max,
        nonopaque_pixels=nonopaque_pixels, alpha_content_box=alpha_content_box,
        corner_alpha_max=corner_alpha_max, corner_luma_range=corner_range,
        edge_luma_range=edge_range, preview_mask=PLATFORM_MASKS[platform],
        findings=findings, preview_files=preview_files,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preflight an app-icon bitmap and optionally create platform-aware previews.")
    parser.add_argument("source", type=Path, help="PNG, JPEG, or other Pillow-readable image")
    parser.add_argument("--platform", choices=sorted(PLATFORM_SPECS), default="ios")
    parser.add_argument("--role", choices=("concept", "flattened", "layer"), default="flattened")
    parser.add_argument("--allow-nonstandard", action="store_true", help="Downgrade a platform-dimension mismatch from error to warning")
    parser.add_argument("--preview-dir", type=Path, help="Directory for size previews and an appearance sheet")
    parser.add_argument("--sizes", type=parse_sizes, default=DEFAULT_PREVIEW_SIZES, help="Comma-separated preview widths")
    parser.add_argument("--expected-content-box", type=parse_box, help="For a layer: allowed alpha bounds as left,top,right,bottom")
    parser.add_argument("--report", type=Path, help="Write the JSON audit to this path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.source.is_file():
        print(f"error: source not found: {args.source}", file=sys.stderr)
        return 2
    audit = audit_image(args.source, args.platform, args.role, args.allow_nonstandard, args.preview_dir, args.sizes, args.expected_content_box)
    output = json.dumps(audit.to_dict(), indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if audit.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
