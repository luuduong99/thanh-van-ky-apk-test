#!/usr/bin/env python3
"""Guard against using a pending preview or old proxy as production character art."""
import argparse
import json
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[2] / 'docs/art/LAM_THIEN_DESIGN_REGISTRY.json'


def validate(data):
    errors=[]
    approved=data.get('latest_user_approved_design') or {}
    candidate=data.get('latest_pending_preview') or {}
    impl=data.get('implementation') or {}
    if not approved.get('id') or not approved.get('approved_on'):
        errors.append('Missing confirmed current design id/date')
    if not approved.get('required_traits'):
        errors.append('Missing required visual traits')
    if candidate.get('approval_status') not in ('pending','approved','rejected'):
        errors.append('Invalid candidate approval status')
    if candidate.get('approval_status')=='pending' and candidate.get('id')==impl.get('design_reference_id'):
        errors.append('Pending preview cannot become production design reference')
    referenced=impl.get('design_reference_id')
    if referenced and referenced != approved.get('id'):
        errors.append('Production design reference must point at latest approved design')
    if referenced and any(s in referenced.lower() for s in ('proxy','cp317','deprecated','reconstruction')):
        errors.append('Deprecated source cannot become production reference')
    if any(impl.get(k) is True for k in ('sprite_layers_complete','spine_rig_complete','physics_approved','apk_integrated')):
        if not referenced:
            errors.append('Production milestone claimed without approved design reference')
        if not approved.get('visual_reference_location'):
            errors.append('Production milestone claimed before current visual asset is recovered/approved')
    if impl.get('apk_integrated') and not impl.get('spine_rig_complete'):
        errors.append('Cannot claim APK integration without rig complete')
    if impl.get('physics_approved') and not impl.get('spine_rig_complete'):
        errors.append('Cannot claim physics approved without rig complete')
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('registry',nargs='?',type=Path,default=DEFAULT)
    args=p.parse_args()
    errors=validate(json.loads(args.registry.read_text(encoding='utf8')))
    if errors:
        print('DESIGN REGISTRY INVALID:\n'+'\n'.join('- '+e for e in errors))
        return 1
    print('DESIGN REGISTRY VALID: current confirmed design specified; CP318 pending, no rig/APK claims')
    return 0

if __name__=='__main__':
    raise SystemExit(main())