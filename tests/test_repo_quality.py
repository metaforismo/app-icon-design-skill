from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_repo.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_repo", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RepositoryQualityTests(unittest.TestCase):
    def test_repository_validator_passes(self) -> None:
        module = load_validator()
        result = module.run()
        self.assertEqual([], result.errors)


if __name__ == "__main__":
    unittest.main()
