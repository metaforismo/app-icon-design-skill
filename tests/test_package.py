from __future__ import annotations

import hashlib
import importlib.util
import sys
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGER = ROOT / "scripts" / "package_skill.py"


def load_packager():
    spec = importlib.util.spec_from_file_location("package_skill", PACKAGER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PackageTests(unittest.TestCase):
    def test_archive_is_deterministic_and_installable(self) -> None:
        module = load_packager()
        first = module.build_archive().read_bytes()
        second = module.build_archive().read_bytes()
        self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest())
        with zipfile.ZipFile(module.ARCHIVE) as archive:
            names = archive.namelist()
        self.assertIn("design-app-icons/SKILL.md", names)
        self.assertIn("design-app-icons/scripts/icon_qa.py", names)
        self.assertFalse(any("__pycache__" in name for name in names))


if __name__ == "__main__":
    unittest.main()
