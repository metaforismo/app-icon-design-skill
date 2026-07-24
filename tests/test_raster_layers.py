from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PREPARE = ROOT / "skills" / "design-app-icons" / "scripts" / "prepare_raster_layer.py"


def load_prepare():
    spec = importlib.util.spec_from_file_location("prepare_raster_layer", PREPARE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RasterLayerTests(unittest.TestCase):
    def test_key_color_becomes_transparent(self) -> None:
        module = load_prepare()
        source = Image.new("RGB", (8, 8), (0, 255, 0))
        for x in range(2, 6):
            for y in range(2, 6):
                source.putpixel((x, y), (120, 40, 170))

        keyed = module.key_to_alpha(source, (0, 255, 0), threshold=70, feather=55)
        self.assertEqual(0, keyed.getpixel((0, 0))[3])
        self.assertEqual(255, keyed.getpixel((3, 3))[3])

    def test_fit_content_uses_shared_canvas(self) -> None:
        module = load_prepare()
        source = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
        source.putpixel((4, 4), (255, 0, 0, 255))
        fitted = module.fit_content(source, 32, (8, 8, 24, 24))
        self.assertEqual((32, 32), fitted.size)
        self.assertIsNotNone(fitted.getchannel("A").getbbox())


if __name__ == "__main__":
    unittest.main()
