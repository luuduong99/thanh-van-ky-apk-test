import copy
import json
import unittest

from tools.validate_global_appearance import CATALOGUE, validate

DATA = json.loads(CATALOGUE.read_text(encoding="utf-8"))


class GlobalAppearanceTests(unittest.TestCase):
    def test_current_catalogue(self):
        self.assertEqual(validate(DATA), [])

    def test_rule_is_project_wide(self):
        d = copy.deepcopy(DATA)
        d["appearanceSystem"]["scope"] = "lin_qian_only"
        self.assertTrue(validate(d))

    def test_all_wardrobe_levels_persist_on_pose_change(self):
        d = copy.deepcopy(DATA)
        d["appearanceSystem"]["poseChangePolicy"] = "only_private_fantasy"
        self.assertTrue(validate(d))

    def test_missing_art_cannot_default(self):
        d = copy.deepcopy(DATA)
        d["appearanceSystem"]["missingArtPolicy"] = "fallback_to_default"
        self.assertTrue(validate(d))

    def test_each_character_has_final_state(self):
        d = copy.deepcopy(DATA)
        d["characters"][0]["wardrobeStates"].pop()
        self.assertTrue(validate(d))

    def test_damage_matrix_required_for_every_wardrobe(self):
        d = copy.deepcopy(DATA)
        d["characters"][1]["wardrobeStates"][0]["integrityImages"]["30"].pop("bed_recline")
        self.assertTrue(validate(d))

    def test_future_character_needs_same_rules(self):
        d = copy.deepcopy(DATA)
        d["characters"].append({"id": "new_heroine", "poses": [], "wardrobeStates": []})
        self.assertTrue(validate(d))

    def test_planned_poses_require_asset_status(self):
        d = copy.deepcopy(DATA)
        d["characters"][0]["plannedPoses"][0]["status"] = "ready"
        self.assertTrue(validate(d))


if __name__ == "__main__":
    unittest.main()
