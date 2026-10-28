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

    def test_backlog_matches_all_registered_characters(self):
        backlog_path = CATALOGUE.parents[4] / "docs/art/GLOBAL_CHARACTER_ASSET_BACKLOG.json"
        backlog = json.loads(backlog_path.read_text(encoding="utf-8"))
        chars = {c["character_id"]: c for c in backlog["characters"]}
        self.assertEqual(set(chars), {c["id"] for c in DATA["characters"]})
        total = 0
        for character in DATA["characters"]:
            expected = (len(character["poses"]) + len(character["plannedPoses"])) * \
                       len(character["wardrobeStates"]) * len(DATA["appearanceSystem"]["integrityLevels"])
            self.assertEqual(chars[character["id"]]["required_combinations"], expected)
            total += expected
        self.assertEqual(backlog["total_required_combinations"], total)

    def test_android_store_is_generic_and_not_pose_scoped(self):
        app = CATALOGUE.parents[1] / "java/vn/thanhvanky/prototype"
        store = (app / "CharacterAppearanceState.kt").read_text(encoding="utf-8")
        activity = (app / "CharacterInteractionActivity.kt").read_text(encoding="utf-8")
        self.assertIn("prefKey(id, \"wardrobe\")", store)
        self.assertIn("prefKey(id, \"integrity\")", store)
        self.assertIn("fun resolveArt(", store)
        self.assertIn("CharacterAppearanceState.resolveArt(", activity)
        self.assertIn("CharacterAppearanceState.setPose(", activity)


if __name__ == "__main__":
    unittest.main()
