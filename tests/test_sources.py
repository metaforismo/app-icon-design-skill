from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_sources.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_sources", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SourceManifestTests(unittest.TestCase):
    def test_official_manifest_is_valid(self) -> None:
        module = load_checker()
        manifest = module.load_manifest(ROOT / "docs" / "source-manifest.yaml")
        self.assertGreaterEqual(len(manifest["sources"]), 10)
        self.assertTrue(all(source["authority"] == "Apple" for source in manifest["sources"]))


if __name__ == "__main__":
    unittest.main()
