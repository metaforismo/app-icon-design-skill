from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "design-app-icons"


class ApprovalGateTests(unittest.TestCase):
    def test_skill_forbids_production_before_explicit_approval(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Do not generate isolated components", text)
        self.assertIn("Do not infer approval from silence", text)
        self.assertIn("Gate A — Lock visual approval", text)

    def test_shipping_apple_icon_uses_composer(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Icon Composer as the final authoring route", text)
        self.assertIn("Gate B — Decide whether the design can become a faithful Composer icon", text)
        self.assertIn("Use the actual Apple app", text)

    def test_exploration_is_bounded_and_versioned(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("one direction", text)
        self.assertIn("two genuinely different directions", text)
        self.assertIn("Do not automatically generate three directions", text)
        self.assertIn("stable version ID", text)
        self.assertTrue((SKILL / "assets" / "concept-review-template.md").is_file())

    def test_composer_adaptation_returns_for_reapproval(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Composer-adapted production concept", text)
        self.assertIn("return to Gate A", text)
        self.assertIn("Never call degraded decomposition progress", text)

    def test_approval_template_defaults_to_locked_off(self) -> None:
        data = yaml.safe_load(
            (SKILL / "assets" / "design-approval-template.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual("exploring-not-approved", data["status"])
        self.assertFalse(data["approval"]["explicitly_approved"])
        self.assertFalse(data["production_plan"]["authorized"])
        self.assertEqual("unselected", data["production_plan"]["delivery_route"])
        self.assertEqual("unassessed", data["production_plan"]["composer_feasibility"])
        self.assertTrue(data["production_plan"]["composer_adaptation_requires_reapproval"])
        self.assertIn("protected_invariants", data["design_lock"])
        self.assertIn("reapproval_triggers", data["production_plan"])

    def test_layer_contract_requires_approved_artifact(self) -> None:
        data = yaml.safe_load(
            (SKILL / "assets" / "layer-composition-template.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual("approved-production-authorized", data["approval"]["state"])
        self.assertIn("approved_concept", data["approval"])
        self.assertIn("sha256", data["approval"])
        self.assertEqual(4, data["composer"]["max_groups"])
        self.assertEqual(["default", "dark", "mono"], data["composer"]["appearances"])


if __name__ == "__main__":
    unittest.main()
