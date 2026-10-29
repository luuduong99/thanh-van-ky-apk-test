import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[2]/"tools").exists() else Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from verify_expression_art_release import validate, flatten_sprites

CANON_SHA="41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711"
EXP_SHA="ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7"
PATH="characters/lin_qian/face/shy_default_100_front.png"
M_PATH="characters/lin_qian/manifest.json"

def digest(raw:bytes)->str:return hashlib.sha256(raw).hexdigest()

class CP335ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.asset=self.root/"app/src/main/assets"
        self.asset.mkdir(parents=True)
        self.profile={"schema_version":1,"characters":[{
            "id":"lin_qian","approval_status":"explicit_user_approved_expression_preview",
            "canonical_body_visual_id":"LT_CANON_BODY_REF_2026-10-28_V2",
            "canonical_body_sha256":CANON_SHA,
            "approved_profile_id":"LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED",
            "expression_preview_sha256":EXP_SHA,
            "approved_expressions":[{"id":v} for v in ("shy","angry","pain","embarrassed","alluring")],
            "sprite_paths":{},
            "production_release":{"status":"blocked_pending_art","artist_qa_passed":False,"runtime_qa_passed":False,
                "user_asset_approval_id":None,"sprite_manifest_path":None,"sprite_manifest_sha256":None,
                "approved_sprite_hashes":{}}
        }]}
        self.save()
    def save(self):
        (self.asset/"character_expression_profiles.json").write_text(json.dumps(self.profile,indent=2),encoding="utf-8")
    def face(self): return self.profile["characters"][0]
    def promote(self):
        target=self.asset/PATH;target.parent.mkdir(parents=True,exist_ok=True)
        img=Image.new("RGBA",(512,512),(255,230,215,0))
        for x in range(70,450):
            for y in range(90,470):img.putpixel((x,y),(200,132,55,255))
        img.save(target)
        mf={"status":"artist_and_user_accepted","canonical_body_visual_id":self.face()["canonical_body_visual_id"]}
        mp=self.asset/M_PATH;mp.write_text(json.dumps(mf),encoding="utf-8")
        self.face()["sprite_paths"]={"shy":{"default":{"100":{"front":PATH}}}}
        self.face()["production_release"]={
            "status":"approved_for_runtime","artist_qa_passed":True,"runtime_qa_passed":True,
            "user_asset_approval_id":"user_asset_signoff_cp335_demo_only",
            "canonical_body_visual_id":self.face()["canonical_body_visual_id"],
            "canonical_body_sha256":CANON_SHA,
            "approved_expression_profile_id":self.face()["approved_profile_id"],
            "approved_expression_sha256":EXP_SHA,
            "sprite_manifest_path":M_PATH,"sprite_manifest_sha256":digest(mp.read_bytes()),
            "approved_sprite_hashes":{PATH:digest(target.read_bytes())}
        }
        self.save()
    def assertBlocked(self,substr):
        errors=validate(self.root)
        self.assertTrue(any(substr in e for e in errors),(substr,errors))
    def test_pending_art_references_are_valid_without_sprite_paths(self):
        self.assertEqual(validate(self.root),[])
    def test_adding_orphan_path_is_blocked(self):
        self.face()["sprite_paths"]={"shy":{"default":{"100":{"front":PATH}}}}
        self.save();self.assertBlocked("without production approval")
    def test_fixture_with_complete_approval_and_real_asset_passes(self):
        self.promote();self.assertEqual(validate(self.root),[])
    def test_user_art_acceptance_is_not_optional(self):
        self.promote();self.face()["production_release"]["user_asset_approval_id"]=None
        self.save();self.assertBlocked("missing explicit user art acceptance")
    def test_manifest_sha_mismatch_is_blocked(self):
        self.promote();(self.asset/M_PATH).write_text('{"fake":"overwrite"}')
        self.assertBlocked("manifest SHA256 mismatch")
    def test_wrong_or_modified_png_is_blocked(self):
        self.promote();(self.asset/PATH).write_bytes(b"corrupt PNG")
        self.assertBlocked("SHA256 mismatch")
    def test_wrong_canon_release_is_blocked(self):
        self.promote();self.face()["production_release"]["canonical_body_sha256"]="0"*64
        self.save();self.assertBlocked("source references differ")
    def test_no_artist_or_runtime_quality_check_is_blocked(self):
        self.promote();self.face()["production_release"]["runtime_qa_passed"]=False
        self.save();self.assertBlocked("runtime_qa_passed must be true")
    def test_path_traversal_is_blocked(self):
        self.promote();self.face()["sprite_paths"]["shy"]["default"]["100"]["front"]="characters/lin_qian/../bad.png"
        self.save();self.assertBlocked("approved sprite list differs")
    def test_same_png_reused_for_different_damage_is_blocked(self):
        self.promote();self.face()["sprite_paths"]["shy"]["default"]["70"]={"front":PATH}
        self.save();self.assertBlocked("one PNG reused for multiple")
    def test_non_rgba_image_is_blocked(self):
        self.promote()
        im=Image.new("RGB",(512,512),(60,90,80));im.save(self.asset/PATH)
        self.face()["production_release"]["approved_sprite_hashes"][PATH]=digest((self.asset/PATH).read_bytes())
        self.save();self.assertBlocked("RGBA PNG")
    def test_too_small_native_asset_is_blocked(self):
        self.promote()
        im=Image.new("RGBA",(250,250),(30,60,80,180));im.save(self.asset/PATH)
        self.face()["production_release"]["approved_sprite_hashes"][PATH]=digest((self.asset/PATH).read_bytes())
        self.save();self.assertBlocked("insufficient native pixels")
    def test_fully_opaque_fake_alpha_is_blocked(self):
        self.promote()
        im=Image.new("RGBA",(512,512),(30,60,80,255));im.save(self.asset/PATH)
        self.face()["production_release"]["approved_sprite_hashes"][PATH]=digest((self.asset/PATH).read_bytes())
        self.save();self.assertBlocked("meaningful alpha")
    def test_malformed_integrity_rejected(self):
        values, errors=flatten_sprites({"shy":{"default":{"75":{"front":PATH}}}},"lin_qian")
        self.assertEqual(values,{})
        self.assertTrue(errors)

if __name__=='__main__':unittest.main()