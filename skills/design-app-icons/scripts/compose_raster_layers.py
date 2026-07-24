#!/usr/bin/env python3
"""Composite same-size PNG layers back-to-front and write a flattened PNG proof."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageCms


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layers", nargs="+", type=Path, help="back-to-front PNG files")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    opened = [Image.open(path).convert("RGBA") for path in args.layers]
    size = opened[0].size
    mismatched = [str(path) for path, image in zip(args.layers, opened) if image.size != size]
    if mismatched:
        parser.error(f"all layers must share {size}; mismatched: {', '.join(mismatched)}")

    composite = Image.new("RGBA", size, (0, 0, 0, 0))
    for image in opened:
        composite.alpha_composite(image)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    srgb_profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    composite.convert("RGB").save(args.output, format="PNG", optimize=True, icc_profile=srgb_profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
