#!/usr/bin/env python3
"""Turn a solid-key Imagegen output into a positioned transparent PNG layer."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageCms


def parse_triplet(value: str) -> tuple[int, int, int]:
    parts = tuple(int(part.strip()) for part in value.split(","))
    if len(parts) != 3 or any(part < 0 or part > 255 for part in parts):
        raise argparse.ArgumentTypeError("expected R,G,B values from 0 to 255")
    return parts


def parse_box(value: str) -> tuple[int, int, int, int]:
    parts = tuple(int(part.strip()) for part in value.split(","))
    if len(parts) != 4 or parts[2] <= parts[0] or parts[3] <= parts[1]:
        raise argparse.ArgumentTypeError("expected left,top,right,bottom")
    return parts


def key_to_alpha(
    image: Image.Image,
    key: tuple[int, int, int],
    threshold: float,
    feather: float,
) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = []
    kr, kg, kb = key
    feather = max(feather, 1.0)

    source = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            red, green, blue, _ = source[x, y]
            distance = math.sqrt((red - kr) ** 2 + (green - kg) ** 2 + (blue - kb) ** 2)
            alpha = max(0.0, min(1.0, (distance - threshold) / feather))
            if alpha <= 0:
                pixels.append((0, 0, 0, 0))
                continue

            # Undo a simple key-color mix at antialiased edges to reduce green spill.
            clean_red = max(0, min(255, round((red - (1 - alpha) * kr) / alpha)))
            clean_green = max(0, min(255, round((green - (1 - alpha) * kg) / alpha)))
            clean_blue = max(0, min(255, round((blue - (1 - alpha) * kb) / alpha)))
            pixels.append((clean_red, clean_green, clean_blue, round(alpha * 255)))

    rgba.putdata(pixels)
    return rgba


def fit_content(
    image: Image.Image,
    canvas_size: int,
    target_box: tuple[int, int, int, int] | None,
) -> Image.Image:
    alpha = image.getchannel("A")
    content_box = alpha.getbbox()
    if not content_box:
        raise ValueError("no foreground survived chroma-key removal")

    content = image.crop(content_box)
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    if target_box is None:
        target_box = (0, 0, canvas_size, canvas_size)

    left, top, right, bottom = target_box
    available = (right - left, bottom - top)
    placed = Image.new("RGBA", available, (0, 0, 0, 0))
    content.thumbnail(available, Image.Resampling.LANCZOS)
    x = (available[0] - content.width) // 2
    y = (available[1] - content.height) // 2
    placed.alpha_composite(content, (x, y))
    canvas.alpha_composite(placed, (left, top))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--key-color", type=parse_triplet, required=True)
    parser.add_argument("--threshold", type=float, default=70.0)
    parser.add_argument("--feather", type=float, default=55.0)
    parser.add_argument("--canvas-size", type=int, default=1024)
    parser.add_argument("--fit-box", type=parse_box)
    parser.add_argument("--report", type=Path, help="Write cleanup geometry and spill metrics as JSON")
    args = parser.parse_args()

    keyed = key_to_alpha(Image.open(args.input), args.key_color, args.threshold, args.feather)
    original_box = keyed.getchannel("A").getbbox()
    if not original_box:
        raise ValueError("no foreground survived chroma-key removal")
    original_width = original_box[2] - original_box[0]
    original_height = original_box[3] - original_box[1]
    target_box = args.fit_box or (0, 0, args.canvas_size, args.canvas_size)
    scale = min(
        (target_box[2] - target_box[0]) / original_width,
        (target_box[3] - target_box[1]) / original_height,
    )
    output = fit_content(keyed, args.canvas_size, args.fit_box)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    srgb_profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    output.save(args.output, format="PNG", optimize=True, icc_profile=srgb_profile)
    final_box = output.getchannel("A").getbbox()
    semi_transparent = 0
    green_spill_candidates = 0
    output_pixels = output.load()
    for y in range(output.height):
        for x in range(output.width):
            red, green, blue, alpha = output_pixels[x, y]
            if 0 < alpha < 255:
                semi_transparent += 1
                if green > red * 1.35 and green > blue * 1.35:
                    green_spill_candidates += 1
    report = {
        "input": str(args.input),
        "output": str(args.output),
        "key_color": args.key_color,
        "threshold": args.threshold,
        "feather": args.feather,
        "original_alpha_box": original_box,
        "target_box": target_box,
        "scale_factor": scale,
        "final_alpha_box": final_box,
        "semi_transparent_pixels": semi_transparent,
        "green_spill_candidate_pixels": green_spill_candidates,
        "limitations": [
            "Spill detection is a simple green-dominance heuristic, not perceptual matting proof.",
            "Fit-box positioning does not prove internal geometry alignment.",
            "Inspect edges over black, white, gray, and saturated backgrounds before import.",
        ],
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
