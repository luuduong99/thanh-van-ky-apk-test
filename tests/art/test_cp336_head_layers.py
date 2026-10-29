"""CP336 real-file tests: 2 angles, 5 expressions, actual 138 PNGs per fixture."""
import copy,hashlib,json,shutil,tempfile,unittest,sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[2]/'tools'/'cp336').exists() else Path(__file__).resolve().parents[1]
TOOL_DIR=(ROOT/'tools'/'cp336') if (ROOT/'tools'/'cp336').exists() else ROOT/'tools'
sys.path.insert(0,str(TOOL_DIR))
from validate_head_layers import validate,PARTS,IDS,VIEWS,MASTER,CANON,APPROVED

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make_fixture(base):
    base=Path(base);(base/'art').mkdir(parents=True,exist_ok=True)
    manifest={'schema_version':1,'character_id':'lin_qian','canonical_body_sha256':CANON,
              'approved_expression_sha256':APPROVED,'production_release':{'status':'blocked_pending_art',
              'artist_qa_passed':False,'runtime_qa_passed':False,'user_asset_approval_id':None},
              'views':{}}
    N=128
    for view in VIEWS:
        vv={'canvas_px':[N,N],'face_attachment_roi_xyxy':[14,22,110,118],
            'underpaint_skin_roi_xyxy':[40,40,80,85], 'master_layers':{},'expressions':{}}
        def write(k,path,color,rect,ellipse=True):
            im=Image.new('RGBA',(N,N),(0,0,0,0));d=ImageDraw.Draw(im)
            if ellipse:d.ellipse(rect,fill=color)
            else:d.rectangle(rect,fill=color)
            out=base/path;out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
            return {'path':str(path).replace('\\','/'),'sha256':sha(out)}
        for i,k in enumerate(MASTER):
            box=[20+i*5,22+i*5,100-i*4,100-i*2]
            if k=='face_underpaint':box=[22,18,104,120]
            color=(239,207,194,255) if k=='face_underpaint' else ((201,204,230,255) if k!='ornament' else (225,171,80,255))
            rel=Path('art')/view/'master'/f'{k}.png'
            vv['master_layers'][k]=write(k,rel,color,box,k!='face_underpaint')
        for idx,e in enumerate(IDS):
            parts={}
            for p in PARTS:
                i=PARTS.index(p)
                if p.endswith('left'):x=36
                elif p.endswith('right'):x=80
                else:x=58
                if p.startswith('iris_'): color=(205,126,54,255);y=57
                elif p.startswith('eye_white'):color=(249,245,243,255);y=53
                elif p.startswith('blush_'):color=(234,137,145,170);y=77
                elif p=='mouth':color=(172,78,83,255);y=98+idx
                else:color=(105,78,97,255);y=40+(i%3)*4+idx
                rel=Path('art')/view/e/f'{p}.png'
                parts[p]=write(p,rel,color,[x-3,y-2,x+3,y+2])
            vv['expressions'][e]=parts
        manifest['views'][view]=vv
    (base/'face_art_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

class HeadLayerFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=tempfile.TemporaryDirectory(prefix='cp336_base_')
        cls.ref=Path(cls.root.name);make_fixture(cls.ref)
    @classmethod
    def tearDownClass(cls):cls.root.cleanup()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='cp336_test_')
        self.p=Path(self.tmp.name)
        shutil.copytree(self.ref,self.p,dirs_exist_ok=True)
        self.mf=self.p/'face_art_manifest.json';self.m=json.loads(self.mf.read_text())
    def tearDown(self):self.tmp.cleanup()
    def save(self):self.mf.write_text(json.dumps(self.m,indent=2)+'\n')
    def changed(self,view,expr,part,action):
        rec=self.m['views'][view]['expressions'][expr][part];p=self.p/rec['path']
        im=Image.open(p).convert('RGBA');action(im);im.save(p);rec['sha256']=sha(p);self.save()
    def test_technical_positive_two_angles_five_expressions_actual_pngs(self):
        r=validate(self.p)
        self.assertTrue(r['ok'],r['errors'])
        self.assertEqual(r['views_checked'],2)
        self.assertEqual(r['layers_read'],2*(4+5*13))
    def test_strict_rejects_unapproved_and_false_high_resolution(self):
        r=validate(self.p,strict=True)
        self.assertFalse(r['ok']);self.assertTrue(any('Art release remains BLOCKED' in e for e in r['errors']))
        self.assertTrue(any('below 1024px' in e for e in r['errors']))
    def test_wrong_canon_checksum_rejected(self):
        self.m['canonical_body_sha256']='0'*64;self.save();self.assertFalse(validate(self.p)['ok'])
    def test_missing_iris_right_rejected(self):
        del self.m['views']['front']['expressions']['angry']['iris_right'];self.save()
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('expected exactly 13' in e for e in r['errors']))
    def test_blue_iris_rejected_even_when_sha_matches(self):
        def blue(im):ImageDraw.Draw(im).rectangle((32,54,40,60),fill=(44,101,212,255))
        self.changed('front','shy','iris_left',blue)
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('amber iris heuristic failed' in e for e in r['errors']))
    def test_opaque_feature_outside_roi_rejected(self):
        self.changed('three_quarter','pain','mouth',lambda im: im.putpixel((0,0),(200,100,100,255)))
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('outside face attachment ROI' in e for e in r['errors']))
    def test_underpaint_hole_rejected(self):
        rec=self.m['views']['front']['master_layers']['face_underpaint'];p=self.p/rec['path']
        im=Image.open(p);ImageDraw.Draw(im).rectangle((39,39,85,90),fill=(0,0,0,0));im.save(p)
        rec['sha256']=sha(p);self.save()
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('holes in base underpaint' in e for e in r['errors']))
    def test_rgba_required_even_if_rgb_png_has_valid_sha(self):
        rec=self.m['views']['front']['expressions']['alluring']['mouth'];p=self.p/rec['path']
        Image.open(p).convert('RGB').save(p);rec['sha256']=sha(p);self.save()
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('needs real PNG RGBA' in e for e in r['errors']))
    def test_path_traversal_rejected(self):
        self.m['views']['front']['master_layers']['hair_front']['path']='art/../../secrets.png';self.save()
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('Unsafe' in e for e in r['errors']))
    def test_file_modification_detected_by_sha(self):
        rec=self.m['views']['front']['expressions']['shy']['mouth'];p=self.p/rec['path']
        p.write_bytes(p.read_bytes()+b'corrupted')
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('checksum mismatch' in e for e in r['errors']))
    def test_changing_view_canvas_rejected(self):
        self.m['views']['front']['canvas_px']=[512,512];self.save()
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('dimensions differ' in e for e in r['errors']))
    def test_both_angles_required(self):
        del self.m['views']['three_quarter'];self.save()
        r=validate(self.p);self.assertFalse(r['ok']);self.assertTrue(any('Both front and three_quarter' in e for e in r['errors']))

if __name__=='__main__':unittest.main()