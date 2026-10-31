# CHAR-CP420 — Lâm Thiển: nghiệm thu master vẽ thật và keyframe CANON (TVK-01)

**Ngày:** 2026-10-31  
**Thread/branch:** TVK-01 · `tvk/characters`  
**Trạng thái:** `ART_REWORK_REQUIRED` / `BLOCKED_PENDING_PAINTED_MASTER` — chưa có keyframe production được nghiệm thu  
**Mốc trước:** CP419 chỉ là Android DEBUG same-pose, bitmap mesh + blink DRAFT; không coi là rig/art phát hành.

## 1. Nguồn khóa & điều đã trực tiếp xác minh

- CANON đã được người dùng duyệt: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` — **941 × 1672 RGBA**, raw SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Ngày 2026-10-31, đọc bản gốc từ Library `/Thanh Van Ky/Approved References/Lam_Thien_CANON_V2_1_FINAL_20261029/`, kiểm trực tiếp raw SHA, kích thước và color mode: **3/3 checks PASS**.
- Front standing chỉ là crop pixel nguồn `(16,180,224,623)` = **208 × 443**; cắt/phóng không biến nó thành master HD. Hình trên sheet có các pose/reference khác; **không** lấy mặt ở ô biểu cảm khác pose để ghép lên nhân vật đứng.
- Bất biến: hình thể **+17%**, nhận diện mặt, tóc bạc tím, hoa/đồ trang sức, trắng–xanh–vàng, cấu trúc trang phục và **hai mũi guốc xanh**. Các tư thế/trang phục tham khảo không được lén thay CANON.
- Chưa xác minh được bất kỳ **master painted high-res tách lớp cùng pose** nào có art approval; không gán trạng thái APPROVED vì kiểm tra file gốc thành công.

## 2. Quyết định mới từ nhánh tích hợp — BẮT BUỘC

Theo `docs/team/STATIC_FIRST_SCENE_MODE.md` và cập nhật 2026-10-31 ở `docs/PROJECT_SPEC.md`:

1. **Static-first / view-only** trong gameplay: nhân vật render tĩnh không méo; không body touch zones. Nút chọn cảnh, tư thế, trang phục, biểu cảm và map/dialogue tiếp tục hoạt động.
2. **Cấm** warp toàn hình, `drawBitmapMesh`, scale/stretch cục bộ ngực/vai/mặt/tóc hoặc xoay/cắt patch ảnh phẳng rồi gọi là micro-animation; video motion kiểu kéo ảnh đã bị người dùng **REJECTED**.
3. CP419 và các viewer cũ chỉ còn dùng ở **DEBUG**, không tự đưa lên màn sản phẩm.
4. Chuyển động chỉ sử dụng **frame độc lập được vẽ riêng** có underpaint thật, đáp ứng visual QA của người dùng; nếu thiếu hình phù hợp thì **fallback static**, không tự thay pose/model.

## 3. Kế hoạch sản xuất art thực cho CHAR-CP420

**Mốc A (ưu tiên duy nhất hiện tại):** vẽ lại front standing high-resolution theo đúng CANON (target đề xuất theo master asset plan: **2160 × 3840 RGBA, 9:16**, nhưng phải là tranh được vẽ lại sắc nét thực chất, KHÔNG phải AI-upscale/resize ảnh 208×443). Cần file chỉnh sửa được (Krita/ORA/PSD) với ít nhất các lớp tách có ngữ nghĩa: `head_face`, `eyes_open`, `eyes_closed_painted`, `hair_front`, `hair_back`, `scalp_nape_underpaint`, `neck_underpaint`, `upper_body_skin`, `bodice_and_folds`, `ornaments`. Layer dưới vùng che phải có màu/nét phù hợp và alpha sạch. Neutral composition giữ đúng pose, tỷ lệ và nhận diện CANON.

**Mốc B (sau khi Mốc A đạt visual QA):** vẽ **2–4 keyframe riêng biệt** cùng canvas/pose; ưu tiên nhịp thở và vải vùng ngực (cùng nếp áo, ánh sáng, viền trang phục), rồi mới tóc/tay áo/lụa, chớp mắt. Không mô phỏng frame thứ hai bằng co giãn frame đầu. Mỗi frame có thể kiểm tra khi đứng yên. Khi nhắm mắt phải vẽ mí/mi/da đúng khuôn mặt standing, không dán từ ô biểu cảm khác.

**Mốc C:** preview fullbody + zoom ở native, vòng keyframe thời gian chậm, so trực tiếp CANON, xin người dùng duyệt. Chỉ sau đó TVK-04 mới được xét tích hợp animation; Android device QA vẫn là cổng riêng.

### Danh sách bàn giao tối thiểu (KHÔNG khẳng định đã có)

- `LT_MASTER_FRONT_NEUTRAL_v01.ora` + PNG 9:16: master painted edit được, nhận diện CANON.
- `LT_BREATH_KF00_IDLE_v01.png` / `KF01_INHALE` / `KF02_EXHALE` (thứ tự/mốc nhịp tạm thời; 2–4 frame thật sau khi họa sĩ vẽ).
- `LT_HEAD_EYES_OPEN_v01.png` và `LT_HEAD_EYES_CLOSED_v01.png` cùng pose; ẩn/hiện để nghiệm thu.
- `LT_CP420_QA_BOARD_v01.png` gồm nguyên CANON, fullbody draft, cận mặt, cổ/gáy, ngực/vải, tay áo, hai guốc; nhãn `DRAFT_NOT_APPROVED`.
- `LT_CP420_MANIFEST.json` ghi SHA-256 thực từng file, độ phân giải, pose, layer, phân loại DRAFT/APPROVED, bằng chứng duyệt; không tự điền đường dẫn sprite production.

## 4. Tiêu chí ACCEPT / REJECT trước animation và APK

| Gate | Yêu cầu | Trạng thái 2026-10-31 |
|---|---|---|
| SOURCE | Raw CANON SHA + 941×1672 RGBA | **PASS** |
| ART-01 | Master standing full-resolution được vẽ thật, khớp nhận diện CANON | **BLOCKED** |
| ART-02 | Head, hair, nape, neck có lớp thật + underpaint, không halo/khe hở | **BLOCKED** |
| ART-03 | Closed eyelid cùng pose, painter-quality, duyệt ở native và zoom | **BLOCKED** |
| ART-04 | 2–4 keyframe thở/ngực/vải **vẽ riêng**, không warp/scale patch | **BLOCKED** |
| ART-05 | Người dùng duyệt fullbody + zoom + motion trên cùng model | **PENDING_USER** |
| RUNTIME | Static-first, không body hotspots; animation fallback tĩnh | **Quy chuẩn tích hợp đã có; TVK-01 không sửa runtime shared** |
| DEVICE | Android device render / cảm nhận chuyển động thật | **NOT_VERIFIED** |

**Khóa release giữ nguyên:** `sprite_paths={}`, `visual_approval=PENDING_USER`, `spine_ready=false`, `android_device_verified=false`, `production_release.status=blocked_pending_art`.

## 5. Việc đã thực hiện trong checkpoint này / giới hạn

- Đã xác minh byte của ảnh CANON thật tại Library; đối chiếu CP419 và chính sách static-first mới nhất.
- Chưa vẽ master painter-grade hoặc 2–4 keyframe mới; không làm giả kết quả từ việc cắt/resize/mask source, không claim test mỹ thuật đã PASS.
- Thay đổi code/art production: **không**. Handoff này là tiêu chuẩn thực thi và kiểm gate chặn demo kéo ảnh quay lại game.
- Chỉ báo cáo dữ liệu trực tiếp kiểm: SOURCE **3 PASS / 0 FAIL / 0 SKIP**; ART **BLOCKED**, Android device **NOT_VERIFIED**. Không có CI/build mới cho handoff tài liệu.

## 6. Bàn giao cho TVK-04

- Không nhập CP419 fullbody mesh vào gameplay; giữ `ImageView.FIT_CENTER` static và scene controls theo quy chuẩn mới.
- Khi có master painted + keyframes có SHA và visual approval, TVK-01 gửi PR nhỏ gồm manifest, asset đủ quyền sử dụng, QA; TVK-04 kiểm riêng Android và fallback.
- **Bước thật tiếp theo của TVK-01:** sản xuất *first painted neutral front master* từ CANON đúng pose, cho xem trực tiếp và xin duyệt; không mở CP421 chỉ để sinh thêm pixel mask/debug.
