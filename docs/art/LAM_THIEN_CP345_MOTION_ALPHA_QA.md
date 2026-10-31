# CP345 — Motion alpha QA

Status: CLI implementation and 3/3 synthetic local tests PASS. No real Lam Thien motion frames tested. Canon V2.1 remains locked; CP344 real underpaint/riggable art remains blocked.

Utility: tools/art/check_motion_alpha.py compares two equal-size RGBA exported frames within a selected joint rectangle. Reports alpha coverage differences for human review. It cannot infer actual holes solely from pose changes, nor prove animation smoothness.

Usage: python tools/art/check_motion_alpha.py idle.png lift.png --region 100,150,120,180 --out report.json

Needs Python, Pillow, NumPy. Next: apply to actual high-resolution layered Front and composite frames, inspect shoulder seam, overlap and approved silhouette manually. Production remains blocked_pending_art.