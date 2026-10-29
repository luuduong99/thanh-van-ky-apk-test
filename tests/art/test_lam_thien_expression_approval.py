"""Guard against changing Lam Thien's approved 5-expression art by accident."""
import copy
import unittest

from tools.validate_lam_thien_expression_approval import load_contracts, validate


class ExpressionApprovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load_contracts()

    def check(self, key, edit):
        data = copy.deepcopy(self.base)
        edit(data[key])
        return validate(data["approved"], data["registry"], data["model"], data["global"])

    def test_current_approved_contract(self):
        self.assertEqual(
            validate(self.base["approved"], self.base["registry"],
                     self.base["model"], self.base["global"]), []
        )

    def test_cannot_drop_one_expression(self):
        errors = self.check("approved", lambda x: x["approved_expressions"].pop())
        self.assertTrue(any("five approved emotions" in e for e in errors))

    def test_cannot_revert_to_pending_status(self):
        errors = self.check("approved", lambda x: x.update(approval_status="pending_user_preview_approval"))
        self.assertTrue(any("approval is missing" in e for e in errors))

    def test_cannot_replace_body_v2(self):
        errors = self.check("registry", lambda x: x["latest_user_approved_design"].update(id="cp322_alpha_draft"))
        self.assertTrue(any("character model V2" in e for e in errors))

    def test_cannot_use_wrong_expression_image(self):
        errors = self.check("approved", lambda x: x["source"].update(sha256="wrong"))
        self.assertTrue(any("SHA256" in e for e in errors))

    def test_cannot_reuse_lam_thien_face_for_other_characters(self):
        errors = self.check("global", lambda x: x["per_character_requirements"].update(no_copying_lam_thien_face_or_body=False))
        self.assertTrue(any("individualized" in e for e in errors))

    def test_cannot_approve_to_nguyet_ly_without_review(self):
        errors = self.check("global", lambda x: x["examples"]["to_nguyet_ly"].update(approved_expression_profile="LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED"))
        self.assertTrue(any("pre-approve" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
