# Thanh Vân Ký — CP412: kiểm tra khe ghép khi nghiêng đầu và gói vẽ cùng pose

**Ngày:** 2026-10-30  
**Nhân vật:** Lâm Thiển  
**Nhánh:** `map-2d-prototype`  
**Trạng thái:** `ARTIST_HANDOFF_BLOCKED_PENDING_TRUE_LAYERED_ART` / NOT APPROVED.

## Khóa nguồn và bài học cần tránh

- Chính xác CANON V2.1 +17% `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Front standing box `(16,180,224,623)` = 208×443 px, **không** phải chân dung expression `(25,684,193,881)` = 168×197. Không được overlay hai pose.
- Nguồn được materialize riêng và kiểm SHA thật trước khi dựng. Không đưa CANON private vào repo public hoặc APK.

## Thành quả CP412 đã tạo thật

1. Từ crop fullbody CANON nguyên pixel, thử `rough head capsule` từ CP411 với góc đầu -4°, -2°, 0°, +2°, +4° và tấm underpaint **tự động chỉ để nghiên cứu**. Bảng `CP412_HEAD_ROTATION_SEAM_DIAGNOSTIC.png` gồm 5 dáng toàn thân và 5 ảnh cận cảnh, không phải hoạt ảnh hoặc asset production.
2. Định lượng pixel bị lộ trong vùng mặt nạ nghiên cứu cần underpaint thật: -4° **271 px**, -2° **174 px**, 0° **0 px**, +2° **174 px**, +4° **276 px** ở ảnh đứng native. Các số này không chấm chất lượng vẽ. Ở 0° ảnh tái ghép đúng pixel nguyên bản CANON.
3. Bản `CP412_ARTIST_INTAKE_BLANK_LAYERS.ora` có **9 layer**: 1 layer nguồn fullbody CANON hiển thị; **8 layer vẽ trống/ẩn** dành cho tóc trước, mặt, mí mắt nhắm cùng pose, tóc dài phía sau, lớp lót cổ/gáy, lót vai, lót tóc và trang sức. Đây không phải nguồn art đã được vẽ hay master HD.
4. Xuất `CP412_FRONT_HEAD_ANNOTATION_4X.png` (zoom NEAREST chỉ để soi); `CP412_CANON_FRONT_UNMODIFIED.png`; JSON manifest khóa nguồn và trạng thái art. Bộ offline có bản CANON byte-exact, script và unittest để dựng lại.
5. **10/10 local unittest PASS** khi nạp CANON thật, gồm source guard, mask, head pivot, neutral exact, exposed-area diagnostics, ORA hidden blank layers và gate `art_approved=false`. CI công khai đã xác minh [GitHub Actions run 41069360009](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41069360009) **SUCCESS: 10 tests discovered, 5 PASS / 5 SKIP** do không có private CANON. Đây là kỹ thuật, không phải duyệt mỹ thuật.

## Không được nhầm với đã hoàn tất

- Tám lớp trống không phải lớp vẽ đã hoàn thành. Vùng kín da/cổ/tóc dưới đầu khi xoay hiện chưa có tác phẩm chính xác.
- Mắt nhắm same-pose artist-quality vẫn thiếu; bài thử CP409 biểu cảm không ghép vào front standing.
- Không có xương đầu/cổ, hair segmentation handpaint, Spine import/acceptance, hay QA Android thiết bị thật.
- Giữ `sprite_paths={}`, `production_release.status=blocked_pending_art`, `spine_ready=false`, `apk_production_ready=false`.

## Điều kiện hoàn thành CP413 tiếp theo

- Có đầu/mặt ở **đúng pose đứng**, vẽ sạch vùng bị che khuất cổ/gáy/tóc và các lớp có thể chuyển động thực tế.
- Có mắt nhắm thật tại góc nhìn đó và preview cạnh CANON ở native/zoom. Người dùng phải xem và duyệt mỹ thuật.
- Hậu nghiệm 0° phải khớp CANON ở vùng cố định; ±2°, ±4° không có đường cắt gãy, rỗng, xuất hiện màu giả hay bóng tóc vẽ sai.
- Chỉ đưa vào rig/Spine/Android khi các lớp được nghiệm thu; tránh tạo thêm checkpoint chỉ test mask mà không sinh art thật.

## Code trên GitHub

- [`tools/art/cp412_same_pose_head_art_gate.py`](../../tools/art/cp412_same_pose_head_art_gate.py)
- [`tests/art/test_cp412_same_pose_head_art_gate.py`](../../tests/art/test_cp412_same_pose_head_art_gate.py)
- `.github/workflows/cp412_same_pose_head_art_gate.yml`

Lưu file private ngoài repo: `/Thanh Van Ky/Development/CP412_Same_Pose_Head_Art_Gate/`. CANON không được gửi lên GitHub public.