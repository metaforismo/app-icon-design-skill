from __future__ import annotations

import importlib.util
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
            self.assertEqual(4, len(audit.preview_files))

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


if __name__ == "__main__":
    unittest.main()
