from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "design-app-icons"


class ApprovalGateTests(unittest.TestCase):
    def test_skill_forbids_production_before_explicit_approval(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("do not create SVG production geometry", text)
        self.assertIn("Do not infer approval from silence", text)
        self.assertIn("Do not begin Icon Composer or Xcode integration for an unapproved concept", text)

    def test_approval_template_defaults_to_locked_off(self) -> None:
        data = yaml.safe_load(
            (SKILL / "assets" / "design-approval-template.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual("exploring-not-approved", data["status"])
        self.assertFalse(data["approval"]["explicitly_approved"])
        self.assertFalse(data["production_plan"]["authorized"])
        self.assertIn("protected_invariants", data["design_lock"])
        self.assertIn("reapproval_triggers", data["production_plan"])

    def test_layer_contract_requires_approved_artifact(self) -> None:
        data = yaml.safe_load(
            (SKILL / "assets" / "layer-composition-template.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual("approved-production-authorized", data["approval"]["state"])
        self.assertIn("approved_concept", data["approval"])
        self.assertIn("sha256", data["approval"])


if __name__ == "__main__":
    unittest.main()
