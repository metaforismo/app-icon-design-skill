from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ICON_QA = ROOT / "skills" / "design-app-icons" / "scripts" / "icon_qa.py"


def load_icon_qa():
    spec = importlib.util.spec_from_file_location("icon_qa", ICON_QA)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class IconQATests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_icon_qa()

    def test_opaque_ios_master_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "icon.png"
            Image.new("RGB", (1024, 1024), "#123456").save(source)
            audit = self.module.audit_image(
                source,
                "ios",
                "flattened",
                False,
                root / "previews",
                (16, 60, 128),
            )
            self.assertTrue(audit.passed)
            self.assertEqual(0, audit.nonopaque_pixels)
            self.assertEqual(5, len(audit.preview_files))
            context_board = Path(audit.preview_files[-1])
            self.assertTrue(context_board.name.endswith("-ios-context-board.png"))
            with Image.open(context_board) as image:
                self.assertEqual((1200, 760), image.size)

    def test_transparent_flattened_master_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "transparent.png"
            Image.new("RGBA", (1024, 1024), (18, 52, 86, 0)).save(source)
            audit = self.module.audit_image(
                source,
                "ios",
                "flattened",
                False,
                None,
                (16,),
            )
            self.assertFalse(audit.passed)
            self.assertIn("alpha", {finding.code for finding in audit.findings})

    def test_watch_dimension_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "watch.png"
            Image.new("RGB", (1024, 1024), "#abcdef").save(source)
            audit = self.module.audit_image(
                source,
                "watchos",
                "flattened",
                False,
                None,
                (16,),
            )
            self.assertFalse(audit.passed)
            self.assertIn("dimensions", {finding.code for finding in audit.findings})

    def test_tvos_previews_preserve_five_by_three_aspect(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "tvos.png"
            Image.new("RGB", (800, 480), "#336699").save(source, icc_profile=b"test-profile")
            audit = self.module.audit_image(source, "tvos", "flattened", False, root / "previews", (100,))
            preview = Path(audit.preview_files[0])
            with Image.open(preview) as image:
                self.assertEqual((100, 60), image.size)
            self.assertEqual("rounded-rectangle", audit.preview_mask)

    def test_round_platform_preview_masks_corners(self) -> None:
        image = Image.new("RGB", (1088, 1088), "#ff0000")
        preview = self.module.render_context_preview(image, 64, "watchos", "dark")
        self.assertEqual((17, 19, 24), preview.getpixel((0, 0)))
        self.assertEqual((255, 0, 0), preview.getpixel((32, 32)))

    def test_non_png_delivery_source_warns(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "icon.jpg"
            Image.new("RGB", (1024, 1024), "white").save(source, "JPEG")
            audit = self.module.audit_image(source, "ios", "flattened", False, None, (16,))
            self.assertTrue(audit.passed)
            self.assertIn("delivery-format", {finding.code for finding in audit.findings})

    def test_opaque_foreground_layer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "fake-alpha.png"
            Image.new("RGB", (1024, 1024), "white").save(source)
            audit = self.module.audit_image(source, "ios", "layer", False, None, (16,))
            self.assertFalse(audit.passed)
            self.assertIn("layer-alpha", {finding.code for finding in audit.findings})

    def test_layer_content_box_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "layer.png"
            image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
            for x in range(100, 300):
                for y in range(100, 300):
                    image.putpixel((x, y), (255, 0, 0, 255))
            image.save(source)
            audit = self.module.audit_image(source, "ios", "layer", False, None, (16,), (120, 120, 320, 320))
            self.assertFalse(audit.passed)
            self.assertIn("content-box", {finding.code for finding in audit.findings})

    def test_empty_layer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "empty.png"
            Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)).save(source)
            audit = self.module.audit_image(source, "ios", "layer", False, None, (16,))
            self.assertFalse(audit.passed)
            self.assertIn("empty-layer", {finding.code for finding in audit.findings})

    def test_cli_writes_machine_readable_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "icon.png"
            report = root / "audit.json"
            Image.new("RGB", (1024, 1024), "#123456").save(source)
            result = subprocess.run(
                [sys.executable, str(ICON_QA), str(source), "--platform", "ios", "--role", "concept", "--report", str(report)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("ios", payload["platform"])
            self.assertEqual("rounded-rectangle", payload["preview_mask"])
            self.assertIn("limitations", payload)


if __name__ == "__main__":
    unittest.main()
